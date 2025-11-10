from django.utils.deprecation import MiddlewareMixin
from django.db import connections


class TimezoneUTCEnforcer(MiddlewareMixin):
    """
    Middleware que força TIME ZONE UTC nas conexões de banco
    ANTES do SessionMiddleware acessar o banco.
    """

    def process_request(self, request):
        # Garante UTC no banco padrão
        try:
            with connections['default'].cursor() as c:
                c.execute("SET TIME ZONE 'UTC'")
                c.execute("SHOW TIME ZONE")
                tz = c.fetchone()[0]
                try:
                    print(f"[TZ] default -> {tz}")
                except Exception:
                    pass
        except Exception as e:
            try:
                print(f"[TZ] Falha ao definir UTC no default: {e}")
            except Exception:
                pass

        # Opcional: garantir UTC nos aliases de cliente já configurados
        for alias in list(connections.databases.keys()):
            if alias.startswith('cliente_'):
                try:
                    with connections[alias].cursor() as c:
                        c.execute("SET TIME ZONE 'UTC'")
                        c.execute("SHOW TIME ZONE")
                        tz = c.fetchone()[0]
                        try:
                            print(f"[TZ] {alias} -> {tz}")
                        except Exception:
                            pass
                except Exception:
                    pass

        return None