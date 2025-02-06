# licencas/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from licencas.models import Licencas, Empresas, Filiais, Usuarios

class DocumentoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Buscar a licença com o documento fornecido (CPF ou CNPJ)
            licenca = Licencas.objects.get(lice_docu=username)
            
            # Verifica se a licença está ativa (não bloqueada)
            if licenca.lice_bloq:
                return None  # Licença bloqueada, não autentica o usuário
            
            # Buscar o usuário associado à licença
            user = Usuarios.objects.get(licenca=licenca, usua_login=username)
            
            # Verifica a senha do usuário
            if user.check_password(password):
                return user  # Retorna o usuário autenticado
        except (Licencas.DoesNotExist, Usuarios.DoesNotExist):
            return None  # Caso não encontre a licença ou o usuário, retorna None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, usua_login=None, usua_senh=None, **kwargs):
        try:
            user = get_user_model().objects.get(usua_login=usua_login)
            if user.check_password(usua_senh):
                # Se for superusuário, permite login sem restrição de documento
                if user.is_superuser:
                    return user
                else:
                    # Se for usuário normal, valida a licença e outras restrições
                    return user
        except get_user_model().DoesNotExist:
            return None
