from django.db import connections
import os
from licencas.utils.licencas_loader import carregar_licencas_dict


def _slug_variants(slug: str):
    s = (slug or "").upper()
    variants = [s]
    # Remover sufixos societários comuns para casar chaves como CASAEALMA
    for suf in ("LTDA", "ME", "EPP", "SA", "S/A", "EIRELI"):
        if s.endswith(suf):
            variants.append(s[: -len(suf)])
    return [v for v in variants if v]


def _resolve_client_env(info: dict):
    """Resolve USER/PASSWORD/HOST/PORT por cliente a partir do .env.
    Prioridade:
    1) <SLUG>_DB_* (com variantes sem sufixos societários)
    2) <DBNAME>_DB_*
    3) globais DB_*
    """
    slug = (info.get("slug") or "").strip()
    dbname = (info.get("db_name") or "").strip()
    variants = _slug_variants(slug)

    def first_env(keys):
        for k in keys:
            val = os.getenv(k)
            if val:
                return k, val
        return None, None

    # USER
    user_key, user_val = first_env([f"{v}_DB_USER" for v in variants] + [f"{dbname.upper()}_DB_USER"] + ["DB_USER"])
    # PASSWORD
    pass_key, pass_val = first_env([f"{v}_DB_PASSWORD" for v in variants] + [f"{dbname.upper()}_DB_PASSWORD"] + ["DB_PASSWORD"])
    # HOST/PORT
    host_key, host_val = first_env([f"{v}_DB_HOST" for v in variants] + [f"{dbname.upper()}_DB_HOST"] + ["DB_HOST"])
    port_key, port_val = first_env([f"{v}_DB_PORT" for v in variants] + [f"{dbname.upper()}_DB_PORT"] + ["DB_PORT"])

    return {
        "USER": user_val or os.getenv("DB_USER", "savexml"),
        "PASSWORD": pass_val or os.getenv("DB_PASSWORD", ""),
        "HOST": host_val or os.getenv("DB_HOST", "base.rtalmeida.com.br"),
        "PORT": port_val or os.getenv("DB_PORT", "5432"),
        "_sources": {
            "USER": user_key or "DB_USER",
            "PASSWORD": pass_key or "DB_PASSWORD",
            "HOST": host_key or "DB_HOST",
            "PORT": port_key or "DB_PORT",
        },
    }

class LicencaDBRouter:
    _cache = None

    def _get_licenca(self, slug):
        if not self._cache:
            self._cache = {x["slug"]: x for x in carregar_licencas_dict()}
        return self._cache.get(slug)

    def db_for_read(self, model, **hints):
        slug = hints.get("slug")
        if not slug:
            return "default"

        lic = self._get_licenca(slug)
        if not lic:
            return "default"

        alias = f"cliente_{slug}"
        if alias not in connections.databases:
            env_conf = _resolve_client_env({"slug": slug, "db_name": lic["db_name"]})
            connections.databases[alias] = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": lic["db_name"],
                "HOST": env_conf["HOST"],
                "PORT": env_conf["PORT"],
                "USER": env_conf["USER"],
                "PASSWORD": env_conf["PASSWORD"],
            "OPTIONS": {"options": "-c TimeZone=UTC"},
            }
            try:
                print(
                    f"[ROUTER] Alias {alias} usando USER={env_conf['USER']} via {env_conf['_sources']['USER']} HOST={env_conf['HOST']} PORT={env_conf['PORT']}"
                )
            except Exception:
                pass
        return alias

    db_for_write = db_for_read
