import threading
import weakref

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
