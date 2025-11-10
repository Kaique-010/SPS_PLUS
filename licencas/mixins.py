from django.conf import settings
from django.db import connections
from django.http import Http404
from licencas.utils import current_alias, current_slug
from licencas.utils.licencas_loader import carregar_licencas_dict

class LicenseDatabaseMixin:
    """
    Mixin para configurar o banco de dados com base na licença do usuário.
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_database_based_on_license()

    def set_database_based_on_license(self):
        # Obtém o slug atual priorizando usuário e depois sessão
        slug = current_slug(self.request)
        if not slug:
            raise Http404("Licença não encontrada para roteamento.")
        lic_map = {x["slug"]: x for x in carregar_licencas_dict()}
        info = lic_map.get(slug)
        if not info:
            raise Http404("Licença não mapeada para roteamento.")

        alias = current_alias(self.request)
        if alias not in connections.databases:
            connections.databases[alias] = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": info["db_name"],
                "HOST": info["db_host"],
                "PORT": info["db_port"],
                "USER": settings.DATABASES["default"]["USER"],
                "PASSWORD": settings.DATABASES["default"]["PASSWORD"],
            "OPTIONS": {"options": "-c TimeZone=UTC"},
            }

        # Disponibiliza o alias para as views
        self.request.db_alias = alias

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