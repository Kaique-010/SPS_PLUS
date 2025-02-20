from django.core.exceptions import ValidationError, PermissionDenied, ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from sps_plus import settings

class LicenseMixin:
    def get_license(self):
        """Obtém a licença do usuário autenticado."""
        if not hasattr(self, "request"):
            return None
        return getattr(self.request.user, "licenca", None)

    def configure_db(self):
        """Configura o banco de dados baseado na licença do usuário."""
        self.licenca = self.get_license()
        self.db_name = self.licenca.lice_nome if self.licenca else "default"

        if self.db_name not in settings.DATABASES:
            raise ImproperlyConfigured(f"A conexão '{self.db_name}' não está configurada em settings.DATABASES.")

        print(f"📝 Licença: {self.licenca}, Banco: {self.db_name}")  # Debug

    def set_db(self):
        """Define o banco de dados baseado na licença do usuário."""
        self.configure_db()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.set_db()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Garante que o formulário seja salvo no banco correto da licença."""
        if not self.request.user.is_authenticated:
            raise ValidationError("Usuário não autenticado.")

        if not self.licenca:
            raise ValidationError("Usuário não tem licença associada.")

        form.instance.licenca = self.licenca
        form.instance.save(using=self.db_name)
        print(f"🔹 Licença salva no banco: {self.db_name}, Licença: {self.licenca}")

        return super().form_valid(form)

    def get_queryset(self):
        """Garante que a listagem seja feita no banco correto."""
        queryset = super().get_queryset().using(self.db_name)
        print(f"📌 Listando dados do banco: {self.db_name}")  # Debug
        return queryset

    def delete_object(self, obj):
        """Método para deletar o objeto no banco correto."""
        print(f"🗑️ Tentando deletar {obj} do banco {self.db_name}")

        # Verifica se o objeto pertence à licença do usuário atual
        if obj.licenca != self.licenca:
            raise PermissionDenied("Você não tem permissão para excluir este objeto.")

        # Verifica se o objeto existe no banco antes da exclusão
        if not self.model.objects.using(self.db_name).filter(id=obj.id).exists():
            print("⚠️ Objeto não encontrado para exclusão.")
            return

        try:
            obj.delete(using=self.db_name)
            print(f"Objeto {obj} deletado com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar excluir objeto: {e}")

        # Verifica se o objeto ainda existe no banco após a exclusão
        exists_after = self.model.objects.using(self.db_name).filter(id=obj.id).exists()
        print(f"Depois da exclusão: {exists_after}")
