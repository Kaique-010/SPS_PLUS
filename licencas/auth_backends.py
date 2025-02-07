# licencas/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from licencas.models import Licencas, Empresas, Filiais, Usuarios

class DocumentoAuthBackend(BaseBackend):
    def authenticate(self, request, lice_docu=None, password=None, **kwargs):
        try:
            # Buscar a licença pelo documento da empresa (lice_docu)
            licenca = Licencas.objects.get(lice_docu=lice_docu)

            # Verificar se a licença está bloqueada
            if licenca.lice_bloq:
                return None

            # Buscar o usuário vinculado à essa licença
            user = Usuarios.objects.get(licenca=licenca, usua_login=lice_docu)

            # Verificar a senha do usuário
            if user.check_password(password):
                return user
        except (Licencas.DoesNotExist, Usuarios.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(lice_docu=username)

            if user.check_password(password):
                if user.is_superuser or not user.licenca.lice_bloq:
                    return user  # Login válido
        except get_user_model().DoesNotExist:
            return None
