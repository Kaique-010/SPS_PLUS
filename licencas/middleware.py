from django.db import connections
from django.http import Http404
from .models import Licencas

class LicenseDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtém a licença da sessão
        licenca_nome = request.session.get("licenca_lice_nome")
        print(f"Licença na sessão: {licenca_nome}")  # Log para depuração

        if licenca_nome:
            try:
                # Carrega as configurações do banco de dados do campo db_config da licença
                licenca = Licencas.objects.using('default').get(lice_nome=licenca_nome)
                print(f"Licença carregada: {licenca}")  # Log para depuração

                if licenca and licenca.db_config:
                    # Obtém o nome do banco de dados da configuração
                    db_name = licenca.db_config.get("NAME")
                    if db_name:
                        # Define o banco de dados ativo para a requisição
                        request.db_alias = db_name  # Usa o nome do banco de dados diretamente
                        print(f"Banco de dados ativo: {request.db_alias}")  # Log para depuração
                    else:
                        print("Erro: Nome do banco de dados não encontrado na configuração.")
            except Licencas.DoesNotExist:
                raise Http404("Licença não encontrada.")
            except Exception as e:
                print(f"Erro ao configurar o banco de dados: {e}")

        # Passa a requisição para o próximo middleware ou view
        response = self.get_response(request)
        return response