def usuario_licenca(request):
    return {
        'usuario_nome': getattr(request, 'usuario_nome', None),
        'licenca_nome': getattr(request, 'licenca_nome', 'Desconhecido')
    }