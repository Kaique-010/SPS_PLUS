import threading
import weakref
from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()

class RequestMiddleware:
    """Armazena o request na thread atual de forma segura"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = weakref.ref(request)  # Armazena um fraco apontador para evitar vazamento de memória
        response = self.get_response(request)
        return response

def get_current_request():
    """Retorna o request atual armazenado na thread"""
    request_ref = getattr(_thread_locals, 'request', None)
    return request_ref() if request_ref else None  # Retorna o request apenas se ainda estiver válido


class DatabaseSelectionMiddleware(MiddlewareMixin):
    """
    Middleware para capturar a escolha do banco de dados pelo superusuário.
    """

    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            # Suponha que o superusuário possa escolher o banco através de uma query string ou algo assim
            selected_db = request.GET.get("db", None)
            if selected_db:
                # Salva na sessão a escolha do banco de dados
                request.session["selected_db"] = selected_db



_thread_locals = threading.local()

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response

def get_current_request():
    return getattr(_thread_locals, "request", None)