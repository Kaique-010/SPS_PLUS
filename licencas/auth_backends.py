# licencas/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from licencas.models import Licencas, Empresas, Filiais, Usuarios

class DocumentoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica um usuário com base no documento da licença.
        """
        # A lógica de autenticação baseada no documento da licença (CPF ou CNPJ)
        try:
            # Buscar a licença com o documento fornecido
            licenca = Licencas.objects.get(lice_docu=username)
            
            # Verifica se a senha corresponde
            # A lógica de senha pode ser ajustada conforme necessário
            if licenca.lice_bloq:
                return None  # Licença bloqueada, não autenticar
                
            # Se a licença for válida, buscar o usuário relacionado
            user = Usuarios.objects.get(licenca=licenca, usua_login=username)
            
            if user.check_password(password):
                return user  # Retorna o usuário autenticado
                
        except (Licencas.DoesNotExist, Usuarios.DoesNotExist) as e:
            return None  # Caso não encontre o usuário ou a licença, retorna None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
