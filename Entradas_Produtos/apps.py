from django.apps import AppConfig


class EntradasProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Entradas_Produtos'

    def ready(self):
        import Entradas_Produtos.signals