from django.core.exceptions import ValidationError
from django.db import connections

class LicenseMixin:
    def get_license(self):
        # Obtém a licença do usuário autenticado
        return self.request.user.licenca

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
            print(f"Banco de dados conectado: {db_name}")

        return super().form_valid(form)

    def set_database_for_license(self, licenca):
        """Define o banco de dados correto para a licença."""
        db_name = licenca.lice_nome
        if db_name and db_name != "default":
            self.set_banco_conectado(licenca)  # Passa o objeto de licença
            print(f"Banco de dados conectado: {db_name}")

    def set_banco_conectado(self, licenca):
        """Define o banco de dados da licença diretamente na sessão."""
        # Armazene o objeto de licença completo na sessão, não apenas o nome
        self.request.session['licenca'] = licenca  # Armazenando o objeto de licença
        self.request.session.modified = True
        print(f"Banco de dados na sessão atualizado para: {licenca.lice_nome}")
