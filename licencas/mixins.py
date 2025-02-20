from django.core.exceptions import ValidationError
from django.db import connections

class LicenseMixin:
    def get_license(self):
        # Obtém a licença do usuário autenticado
        return self.request.user.licenca

    def get_queryset(self):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        return super().get_queryset().using(db_name)

    def form_valid(self, form):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            raise ValidationError("Usuário não autenticado.")

        # Validar se o usuário tem uma licença associada
        licenca = self.get_license()
        if not licenca:
            raise ValidationError("Usuário não tem licença associada.")

        # Definir a licença no formulário antes de salvar
        form.instance.licenca = licenca

        # Definir o banco de dados da licença
        db_name = licenca.lice_nome
        if db_name and db_name != "default":
            self.set_database_for_license(db_name)

        return super().form_valid(form)

    def set_database_for_license(self, db_name):
        """Define o banco de dados correto para a licença."""
        self.set_banco_conectado(db_name)

    def set_banco_conectado(self, db_name):
        """Define o banco de dados da licença diretamente na sessão."""
        self.request.session['licenca_db'] = db_name
        self.request.session.modified = True
