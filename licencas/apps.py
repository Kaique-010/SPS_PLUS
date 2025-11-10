from django.apps import AppConfig

class LicencasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "licencas"

    def ready(self):
        import licencas.signals
        # Desconectar atualização automática de last_login para evitar writes em coluna inexistente
        try:
            from django.contrib.auth.signals import user_logged_in
            from django.contrib.auth.models import update_last_login
            user_logged_in.disconnect(update_last_login)
        except Exception as e:
            # Evitar falha no startup caso estrutura mude
            print(f"Aviso: não foi possível desconectar update_last_login: {e}")

        # Forçar TIME ZONE UTC em todas as conexões ao banco
        try:
            from django.db.backends.signals import connection_created
            from django.db import connections

            def _enforce_utc(sender, connection, **kwargs):
                try:
                    with connection.cursor() as c:
                        c.execute("SET TIME ZONE 'UTC'")
                except Exception as ee:
                    print(f"Aviso: falha ao definir TIME ZONE UTC: {ee}")

            # Aplicar imediatamente nas conexões já conhecidas
            for alias in connections.databases.keys():
                try:
                    with connections[alias].cursor() as c:
                        c.execute("SET TIME ZONE 'UTC'")
                except Exception as ee:
                    # Se a conexão ainda não estiver aberta, será coberta pelo signal
                    pass

            connection_created.connect(_enforce_utc, dispatch_uid="licencas_enforce_utc")
        except Exception as e:
            print(f"Aviso: não foi possível conectar sinal connection_created: {e}")
