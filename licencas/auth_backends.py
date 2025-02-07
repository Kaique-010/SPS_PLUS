from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from licencas.models import Licencas, Usuarios

User = get_user_model()

class DocumentoAuthBackend(BaseBackend):
    def authenticate(self, request, usua_login=None, password=None, **kwargs):
        # Tenta autenticar com base no documento da licença (CNPJ ou CPF)
        try:
            # Verifica se o login corresponde a um documento de licença
            licenca = Licencas.objects.get(lice_docu=usua_login)
            
            # Se a licença for encontrada, verifica se está bloqueada
            if not licenca.lice_bloq:
                print(f"Licença {usua_login} está bloqueada.")
                return None  # Licença bloqueada, não autentica

            # Se não for bloqueada, autentica o usuário associado à licença
            usuario = Usuarios.objects.filter(licenca=licenca).first()
            if usuario and usuario.check_password(password):
                print(f"Usuário {usuario.usua_nome} autenticado com sucesso!")
                return usuario  # Retorna o usuário autenticado com a licença associada
        except Licencas.DoesNotExist:
            print(f"Licença com documento {usua_login} não encontrada.")
        
        # Caso o login não corresponda a uma licença, tenta autenticar com o modelo de usuário normal
        try:
            user = Usuarios.objects.get(usua_login=usua_login)
            if user.check_password(password):
                print(f"Usuário {user.usua_nome} autenticado com sucesso!")
                return user
            else:
                print("Senha incorreta para o usuário.")
        except Usuarios.DoesNotExist:
            print(f"Usuário com login {usua_login} não encontrado.")

        # Se nenhum dos dois casos for encontrado ou as credenciais estiverem incorretas, retorna None
        return None