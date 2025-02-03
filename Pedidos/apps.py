from django.apps import AppConfig

class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Pedidos'

    def ready(self):
        import Pedidos.signals 
