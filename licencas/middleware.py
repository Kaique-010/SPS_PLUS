'''from django.db import connections
from django.http import Http404
from .models import Licencas

class LicenseDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtém a licença da sessão
        licenca_nome = request.session.get("licenca_lice_nome")
        if licenca_nome:
            try:
                # Carrega as configurações do banco de dados do campo db_config da licença
                licenca = Licencas.objects.using('default').get(lice_nome=licenca_nome)
                if licenca and licenca.db_config:
                    # Atualiza a conexão do banco de dados
                    connections['default'].settings_dict.update(licenca.db_config)
            except Licencas.DoesNotExist:
                raise Http404("Licença não encontrada.")
            except Exception as e:
                print(f"Erro ao configurar o banco de dados: {e}")

        # Passa a requisição para o próximo middleware ou view
        response = self.get_response(request)
        return response'''