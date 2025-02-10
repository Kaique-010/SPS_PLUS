from django.utils.deprecation import MiddlewareMixin
from threading import local

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
