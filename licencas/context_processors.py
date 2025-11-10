from licencas.utils import current_slug


def usuario_licenca(request):
    # Obtém o slug/nome da licença priorizando usuário autenticado
    slug = current_slug(request)
    licenca_nome = slug or "Desconhecido"

    # Obtém o nome do usuário
    usuario_nome = getattr(request.user, 'nome', None)

    return {
        'usuario_nome': usuario_nome,
        'licenca_nome': licenca_nome,
    }