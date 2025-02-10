from django.core.exceptions import ValidationError
from django.db import connections

class LicenseMixin:
    def get_license(self):
        # Obtém a licença do usuário autenticado
        return self.request.user.licenca

    def form_valid(self, form):
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

    def set_database_for_license(self, db_name):
        """Define o banco de dados correto para a licença."""
        self.request.session["banco_conectado"] = db_name
        self.request.session.modified = True  # Garante que a sessão seja salva

        # Definir o banco de dados da licença na conexão
        connections.databases['default']['NAME'] = db_name
        
        # Adiciona o banco de dados da licença, se ainda não existir nas conexões
        if db_name not in connections.databases:
            connections.databases[db_name] = connections.databases['default'].copy()
            connections.databases[db_name]['NAME'] = db_name
        
        # Imprimir o banco de dados conectado para diagnóstico
        print(f"Banco de dados definido para: {db_name}")

    def set_banco_conectado(self, licenca):
        """Define o banco de dados da licença diretamente na sessão."""
        self.request.session['banco_conectado'] = licenca.lice_nome
        self.request.session.modified = True  # Garante que a sessão seja salva
        print(f"Banco de dados na sessão atualizado para: {licenca.lice_nome}")
