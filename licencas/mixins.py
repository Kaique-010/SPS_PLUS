from django.conf import settings
from django.db import connections
from django.http import Http404
from .models import Licencas

class LicenseDatabaseMixin:
    """
    Mixin para configurar o banco de dados com base na licença do usuário.
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_database_based_on_license()

    def set_database_based_on_license(self):
        # Obtém a licença da sessão
        licenca_nome = self.request.session.get("licenca_lice_nome")
        if not licenca_nome:
            raise Http404("Licença não encontrada na sessão.")

        # Carrega as configurações do banco de dados do campo db_config da licença
        licenca = Licencas.objects.using('default').get(lice_nome=licenca_nome)
        if licenca and licenca.db_config:
            # Atualiza a conexão do banco de dados
            connections['default'].settings_dict.update(licenca.db_config)
        else:
            raise Http404("Configuração de banco de dados não encontrada para a licença.")

    def form_valid(self, form):
        """
        Método para salvar o objeto no banco de dados configurado.
        """
        # O mixin já configurou o banco de dados, então você pode salvar o objeto normalmente
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        """
        Método para deletar o objeto no banco de dados configurado.
        """
        # O mixin já configurou o banco de dados, então você pode deletar o objeto normalmente
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        """
        Método para obter o queryset no banco de dados configurado.
        """
        # O mixin já configurou o banco de dados, então você pode usar o queryset normalmente
        return self.model.objects.all()