import os
from django.utils.deprecation import MiddlewareMixin
from threading import local
from django.db import connections
from django.utils.deprecation import MiddlewareMixin

from licencas.models import Licencas

_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, "user", None)

class ThreadLocalMiddleware(MiddlewareMixin):
    """ Middleware para armazenar o usuário na thread local """
    def process_request(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            _thread_locals.user = request.user
        else:
            _thread_locals.user = None

def get_current_request():
    return getattr(_thread_locals, "request", None)

class RequestMiddleware(MiddlewareMixin):
    """ Middleware para armazenar a requisição na thread local """
    def process_request(self, request):
        _thread_locals.request = request


class UsuarioLicencaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.usuario_nome = request.user.nome  # Adiciona o nome do usuário na requisição
            request.licenca_nome = request.session.get("licenca_nome", "Desconhecido")  # Adiciona a licença na requisição
        else:
            request.usuario_nome = None
            request.licenca_nome = None

class DatabaseRouterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verifique se a licença está na sessão
        licenca_id = request.session.get('licenca_id')
        if licenca_id:
            # Aqui você deve ter uma lógica para determinar o nome do banco
            # de dados a partir da licença. Exemplo:
            banco_nome = get_database_name_from_license(licenca_id)  # Implemente essa função
            request.licenca = licenca_id
            request.db_name = banco_nome
            
            # Muda a conexão com o banco de dados
            connections['default'].settings_dict['NAME'] = banco_nome
            connections['default'].connect()

def get_database_name_from_license(licenca_id):
    # Implementar lógica para obter o nome do banco de dados associado à licença
    licenca = Licencas.objects.get(id=licenca_id)
    return licenca.lice_nome  # Ajuste conforme sua estrutura



class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está autenticado e se há uma licença selecionada na sessão
        if request.user.is_authenticated and 'selected_licenca_nome' in request.session:
            licenca_nome = request.session['selected_licenca_nome']
            
            try:
                # Buscamos a licença pelo nome
                licenca = Licencas.objects.get(lice_nome=licenca_nome)
                
                # Atualiza a configuração do banco de dados
                connections.databases['default'] = {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': licenca.lice_nome,  # Aqui você define o banco conforme a licença
                    'USER': 'postgres',  # Campos do banco de dados, podem ser alterados para dinâmicos se necessário
                    'PASSWORD': '@spartacus201@',
                    'HOST': "localhost",
                    'PORT': 5433,
                    'ATOMIC_REQUESTS': True,
                    'OPTIONS': {},
                    'CONN_MAX_AGE': 600,
                    'AUTOCOMMIT': True,
                    'CONN_HEALTH_CHECKS': False,
                    'TIME_ZONE': "America/Sao_Paulo",
                }

            except Licencas.DoesNotExist:
                # Se não encontrar a licença, pode redirecionar ou logar erro
                print("Licença não encontrada!")
                # Opção: redirecionar para a seleção de licença ou página de erro
                # return redirect('select-license') 

        response = self.get_response(request)
        return response