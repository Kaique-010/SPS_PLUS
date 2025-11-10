# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import connections
from licencas.utils.licencas_loader import carregar_licencas_dict
import os


def _slug_variants(slug: str):
    s = (slug or "").upper()
    variants = [s]
    for suf in ("LTDA", "ME", "EPP", "SA", "S/A", "EIRELI"):
        if s.endswith(suf):
            variants.append(s[: -len(suf)])
    return [v for v in variants if v]


def _resolve_client_env(info: dict, default_conf: dict):
    slug = (info.get("slug") or "").strip()
    dbname = (info.get("db_name") or "").strip()
    variants = _slug_variants(slug)

    def first_env(keys):
        for k in keys:
            val = os.getenv(k)
            if val:
                return k, val
        return None, None

    user_key, user_val = first_env([f"{v}_DB_USER" for v in variants] + [f"{dbname.upper()}_DB_USER", "DB_USER"])
    pass_key, pass_val = first_env([f"{v}_DB_PASSWORD" for v in variants] + [f"{dbname.upper()}_DB_PASSWORD", "DB_PASSWORD"])
    host_key, host_val = first_env([f"{v}_DB_HOST" for v in variants] + [f"{dbname.upper()}_DB_HOST", "DB_HOST"])
    port_key, port_val = first_env([f"{v}_DB_PORT" for v in variants] + [f"{dbname.upper()}_DB_PORT", "DB_PORT"])

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": info.get("db_name"),
        "HOST": host_val or default_conf.get("HOST") or os.getenv("DB_HOST", "base.rtalmeida.com.br"),
        "PORT": port_val or default_conf.get("PORT") or os.getenv("DB_PORT", "5432"),
        "USER": user_val or default_conf.get("USER") or os.getenv("DB_USER", ""),
        "PASSWORD": pass_val or default_conf.get("PASSWORD") or os.getenv("DB_PASSWORD", ""),
        "OPTIONS": {"options": "-c TimeZone=UTC"},
        "_sources": {
            "USER": user_key or ("default.USER" if default_conf.get("USER") else "DB_USER"),
            "PASSWORD": pass_key or ("default.PASSWORD" if default_conf.get("PASSWORD") else "DB_PASSWORD"),
            "HOST": host_key or ("default.HOST" if default_conf.get("HOST") else "DB_HOST"),
            "PORT": port_key or ("default.PORT" if default_conf.get("PORT") else "DB_PORT"),
        },
    }


class GlobalAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Autentica usando documento (lice_docu) para rotear ao banco correto.
        - Busca mapeamento em licencas2013 no banco default
        - Consulta usuário no alias correspondente
        - Valida por coluna legada usua_senh_mobi em TEXTO PURO
        """
        UserModel = get_user_model()
        if username is None or password is None:
            return None

        # Documento pode vir via kwargs (enviado pelo formulário)
        lice_docu = kwargs.get("lice_docu") if kwargs else None
        # Requisito: documento é obrigatório para autenticar
        if not lice_docu:
            try:
                print("[AUTH] Documento não informado. Autenticação bloqueada pelo requisito de documento.")
            except Exception:
                pass
            return None
        # Mapa de licenças e seleção de candidatos
        by_doc = {x["cnpj"]: x for x in carregar_licencas_dict()}
        candidates = []
        alias = "default"

        if lice_docu:
            # Normaliza documento e define candidato principal
            doc = str(lice_docu).replace(".", "").replace("-", "").replace("/", "").strip()
            info = by_doc.get(doc)
            try:
                print(f"[AUTH] Documento normalizado: {doc} | Info encontrada? {'sim' if info else 'não'}")
            except Exception:
                pass
            if info:
                candidates = [info]
        else:
            # Não deve acontecer porque retornamos acima sem documento
            candidates = []

        # Se não houver candidatos, tenta default minimalmente
        if not candidates:
            candidates = [{
                "slug": "default",
                "db_name": connections.databases.get("default", {}).get("NAME"),
                "db_host": connections.databases.get("default", {}).get("HOST"),
                "db_port": connections.databases.get("default", {}).get("PORT"),
            }]

        user = None
        try:
            print(f"[AUTH] Total de candidatos: {len(candidates)}")
        except Exception:
            pass
        for info in candidates:
            slug = info.get("slug")
            alias = f"cliente_{slug}" if slug and slug != "default" else "default"
            # Resolver credenciais específicas por cliente via .env
            default_conf = connections.databases.get("default", {})
            conn_conf = _resolve_client_env(info, default_conf)
            try:
                print(
                    f"[AUTH] Config alias {alias}: NAME={conn_conf['NAME']} HOST={conn_conf['HOST']} PORT={conn_conf['PORT']} USER_SOURCE={conn_conf['_sources']['USER']}"
                )
            except Exception:
                pass
            # Garante conexão para o alias do cliente
            if alias not in connections.databases and info.get("db_name"):
                connections.databases[alias] = conn_conf
                try:
                    print(f"[AUTH] Alias {alias} adicionado em connections.databases")
                except Exception:
                    pass
            # Testa a conexão ao alias
            try:
                with connections[alias].cursor() as _c:
                    _c.execute("SELECT 1")
                print(f"[AUTH] Conexão ao alias {alias} OK (SELECT 1)")
            except Exception as e:
                try:
                    print(f"[AUTH] ERRO de conexão ao alias {alias}: {e}")
                except Exception:
                    pass
            try:
                print(f"[AUTH] Tentando alias: {alias} para usuario: {username}")
            except Exception:
                pass
            # Busca por nome (USERNAME_FIELD)
            try:
                qs = UserModel.objects.using(alias).filter(**{UserModel.USERNAME_FIELD: username}).order_by('usua_codi')
                user = qs.first()
                try:
                    print(f"[AUTH] Resultado por nome: {'encontrado usua_codi='+str(getattr(user,'usua_codi',None)) if user else 'nenhum'}")
                except Exception:
                    pass
            except Exception as e:
                user = None
                try:
                    print(f"[AUTH] Erro ao buscar por nome no alias {alias}: {e}")
                except Exception:
                    pass
            # Sem coluna 'login' em muitos bancos: focar em usua_nome/usua_codi
            if not user:
                try:
                    with connections[alias].cursor() as cursor:
                        cursor.execute("SELECT usua_codi FROM usuarios WHERE usua_nome = %s ORDER BY usua_codi ASC LIMIT 1", [username])
                        row = cursor.fetchone()
                        if row:
                            user = UserModel.objects.using(alias).filter(usua_codi=row[0]).first()
                            try:
                                print(f"[AUTH] Busca direta por usua_nome: encontrado usua_codi={row[0]}")
                            except Exception:
                                pass
                        else:
                            try:
                                print("[AUTH] Busca direta por usua_nome: nenhum resultado")
                            except Exception:
                                pass
                except Exception as e:
                    user = None
                    try:
                        print(f"[AUTH] Erro na busca direta por usua_nome no alias {alias}: {e}")
                    except Exception:
                        pass
            # Valida senha em TEXTO PURO e retorna
            if user:
                mobile_pwd = getattr(user, "usua_senh_mobi", None) or getattr(user, "password", None)
                if isinstance(mobile_pwd, str):
                    raw = str(password).strip()
                    stored = mobile_pwd.strip()
                    ok = stored == raw
                    try:
                        print(f"[AUTH] Comparando senha (texto puro): stored='{stored}' raw='{raw}' => ok={ok}")
                    except Exception:
                        pass
                    if ok and self.user_can_authenticate(user):
                        # Anexa metadados úteis para sessão
                        try:
                            setattr(user, "_auth_db_alias", alias)
                            if slug and slug != "default":
                                setattr(user, "_cliente_slug", slug)
                                setattr(user, "_cliente_db_name", info.get("db_name"))
                        except Exception:
                            pass
                        try:
                            print(f"[AUTH] Usuário encontrado no alias {alias} (slug={slug}). Autenticado com sucesso.")
                        except Exception:
                            pass
                        return user
                else:
                    try:
                        print("[AUTH] Senha legada não encontrada (usua_senh_mobi nulo ou não-string)")
                    except Exception:
                        pass
            else:
                try:
                    print(f"[AUTH] Usuário não encontrado no alias {alias}")
                except Exception:
                    pass

        # Nada casou
        return None

        # Preferir somente o campo legado em texto puro, sem hash (defensive)
        return None

    def get_user(self, user_id):
        """Recupera o usuário autenticado procurando primeiro no default,
        depois nos aliases de clientes (cliente_*). Isso evita perder a sessão
        quando o usuário foi autenticado em um banco não-default.
        """
        UserModel = get_user_model()
        # Primeiro tenta nos aliases de clientes para evitar capturar um usuário no default por engano
        try:
            from django.db import connections
            aliases = list(connections.databases.keys())
            client_aliases = [a for a in aliases if a.startswith('cliente_')]
            print(f"[AUTH.get_user] Varredura (cliente primeiro): {client_aliases} | depois 'default'")
            for alias in client_aliases:
                try:
                    print(f"[AUTH.get_user] Tentando alias {alias} para user_id={user_id}")
                    user = UserModel.objects.using(alias).get(pk=user_id)
                    print(f"[AUTH.get_user] Encontrado no alias {alias}")
                    return user
                except UserModel.DoesNotExist:
                    print(f"[AUTH.get_user] Não encontrado no alias {alias}")
                    continue
        except Exception as e:
            print(f"[AUTH.get_user] Exceção ao varrer aliases de clientes: {e}")

        # Por fim tenta no default
        try:
            print(f"[AUTH.get_user] Tentando default para user_id={user_id}")
            user = UserModel.objects.get(pk=user_id)
            print("[AUTH.get_user] Encontrado no default")
            return user
        except UserModel.DoesNotExist:
            print("[AUTH.get_user] Não encontrado no default")
        except Exception as e:
            print(f"[AUTH.get_user] Exceção ao consultar default: {e}")

        return None