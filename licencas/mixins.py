from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class DatabaseRouterMixin:
    """
    Mixin para alterar o banco de dados dinamicamente baseado na licença ou empresa do usuário.
    """
    def set_database(self, usuario):
        if usuario.licenca:
            # Acessa a licença associada ao usuário e define a conexão com o banco específico
            licenca_db = usuario.licenca.lice_docu  # ou qualquer atributo que represente a licença
            connection_name = f"db_{licenca_db}"
            # Verifica se a conexão existe no DATABASES
            if connection_name in settings.DATABASES:
                # Altera a conexão para o banco de dados correto
                connections.databases['default'] = settings.DATABASES[connection_name]
            else:
                raise Exception(f"Banco de dados para a licença {licenca_db} não encontrado.")
