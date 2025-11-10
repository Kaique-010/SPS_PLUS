from django.db import connections


def current_slug(request):
    """Retorna o slug do cliente atual.
    Prioriza atributo do usuário autenticado e cai para sessão.
    """
    slug = getattr(request.user, "_cliente_slug", None)
    if slug:
        return slug
    sess_slug = request.session.get("licenca_lice_nome")
    if sess_slug:
        return str(sess_slug).strip().lower().replace(" ", "").replace("-", "")
    return None


def current_alias(request):
    """Retorna o alias de conexão atual (cliente_<slug> ou 'default')."""
    slug = current_slug(request)
    if slug:
        return f"cliente_{slug}"
    return "default"


def current_connection(request):
    """Retorna o objeto de conexão do alias atual."""
    alias = current_alias(request)
    return connections[alias]