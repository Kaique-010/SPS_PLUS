from django.apps import AppConfig


class SaidasProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Saidas_Produtos'
        
    def ready(self):
        import Saidas_Produtos.signals