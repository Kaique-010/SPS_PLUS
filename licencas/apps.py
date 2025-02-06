from django.apps import AppConfig

class LicencasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "licencas"

    def ready(self):
        import licencas.signals  
