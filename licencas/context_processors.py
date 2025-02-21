def usuario_licenca(request):
    # Obtém o nome da licença da sessão
    licenca_nome = request.session.get("licenca_lice_nome", "Desconhecido")
    
    # Obtém o nome do usuário
    usuario_nome = getattr(request.user, 'nome', None)  # Usa o campo 'nome' do usuário

    return {
        'usuario_nome': usuario_nome,
        'licenca_nome': licenca_nome,
    }