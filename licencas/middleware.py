from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from licencas.database_utils import load_databases

from threading import local

_thread_locals = local()

# Mapeamento entre o documento da licença e o nome do banco
LICENCA_DB_MAP = {
    '11111111111111': 'save0',
    '22222222222222': 'lacera',
    # Adicione outros mapeamentos conforme necessário
}

'''class DatabaseRouterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                usuario = request.user

                # Verifique se o usuário é o "master" e usa o banco de dados padrão
                if usuario.usua_login == 'master':
                    connection_name = 'default'  # Banco de dados padrão
                else:
                    if usuario.licenca:
                        licenca_db = usuario.licenca.lice_docu
                        connection_name = LICENCA_DB_MAP.get(licenca_db)

                        if connection_name:
                            if not settings.DATABASES.get(connection_name):
                                load_databases()  # Carrega o banco do JSON se necessário

                            if connection_name in settings.DATABASES:
                                connections.databases['default'] = settings.DATABASES[connection_name]
                            else:
                                raise Exception(f"Banco de dados para a licença {licenca_db} não encontrado.")
                        else:
                            raise Exception(f"Licença {licenca_db} não possui banco de dados mapeado.")
            except Exception as e:
                # Logar o erro para monitoramento e debug
                print(f"Erro ao ajustar o banco de dados: {e}")
                # Pode adicionar algum logging para capturar o erro, ex:
                # logger.error(f"Erro ao ajustar o banco de dados: {e}")
        return None'''

def get_current_request():
    return getattr(_thread_locals, 'request', None)