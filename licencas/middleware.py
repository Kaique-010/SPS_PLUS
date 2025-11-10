from django.utils.deprecation import MiddlewareMixin

class LicencaMiddleware(MiddlewareMixin):
    """
    Injeta o slug do cliente no request.
    Pode vir do path (/api/<slug>/...) ou do header X-Slug.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        slug = view_kwargs.get("slug") or request.headers.get("X-Slug")
        request.slug = slug
        return None
