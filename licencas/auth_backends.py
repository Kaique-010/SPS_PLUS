# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuarios
class GlobalAuthBackend(BaseBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        try:
            user_global = Usuarios.objects.get(login=login)
            if check_password(password, user_global.password):
                return user_global
        except Usuarios.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None