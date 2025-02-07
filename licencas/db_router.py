from django.apps import apps
import os
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS, OperationalError
from licencas.middleware import get_current_request
from licencas.database_utils import save_database, load_databases
from django.db import migrations, connection
from django.core.management import call_command
import json
from datetime import datetime


class LicenseDatabaseRouter:
    """
    Roteador de banco de dados para gerenciar multi-bancos dinâmicos com base na licença do usuário.
    """

    @staticmethod
    def _add_database_to_settings(db_name):
        """Adiciona um banco ao settings.DATABASES e ao JSON."""
        if db_name not in settings.DATABASES:
            settings.DATABASES[db_name] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': os.getenv("DB_USER", "postgres"),
                'PASSWORD': os.getenv("DB_PASSWORD", "@spartacus201@"),
                'HOST': os.getenv("DB_HOST", "localhost"),
                'PORT': os.getenv("DB_PORT", "5433"),
                'ATOMIC_REQUESTS': False,
            }
            save_database(db_name)  # Salva no JSON

    def db_for_read(self, model, **hints):
        """Define o banco para leitura com base na licença do usuário."""
        request = get_current_request()
        if request and hasattr(request, "user") and request.user.is_authenticated:
            # Verifica se o superusuário escolheu um banco específico
            if request.user.is_superuser:
                db_name = request.session.get("selected_db", None)  # A sessão vai armazenar o banco escolhido
                if db_name:
                    return db_name  # Retorna o banco de dados escolhido pelo superusuário

            licenca = getattr(request.user, "licenca", None)
            if licenca:
                db_name = licenca.lice_docu
                self._add_database_to_settings(db_name)
                return db_name

        return DEFAULT_DB_ALIAS

    def db_for_write(self, model, **hints):
        """Define o banco para escrita com base na licença do usuário."""
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Permite migração apenas para bancos cadastrados."""
        return db in load_databases() or db == DEFAULT_DB_ALIAS

    @staticmethod
    def ensure_database_exists(licenca):
        """
        Verifica se o banco de dados existe, caso contrário, cria o banco de dados.
        """
        db_name = licenca.lice_nome

        # Adiciona o banco ao settings se necessário
        LicenseDatabaseRouter._add_database_to_settings(db_name)

        try:
            if not connections[DEFAULT_DB_ALIAS].is_usable():
                connections[DEFAULT_DB_ALIAS].close()
                connections[DEFAULT_DB_ALIAS].connect()

            with connection.cursor() as cursor:
                # Verifica se o banco já existe
                cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
                exists = cursor.fetchone()

                if not exists:
                    # Realiza a criação do banco fora da transação
                    connection.connection.set_isolation_level(0)  # Desativa a transação
                    cursor.execute(f'CREATE DATABASE "{db_name}"')
                    connection.connection.set_isolation_level(1)  # Restaura o nível de isolamento
                    print(f"Banco de dados {db_name} criado com sucesso!")

                    # Aplica as migrações no banco recém-criado
                    LicenseDatabaseRouter.apply_migrations_to_new_db(db_name)

                    # Salva a licença no banco principal (licenças)
                    licenca.save()

        except OperationalError as e:
            print(f"Erro ao criar/verificar o banco {db_name}: {e}")

    @staticmethod
    def apply_migrations_to_new_db(db_name):
        """
        Aplica as migrações no banco de dados recém-criado.
        """
        settings.DATABASES[db_name] = settings.DATABASES[DEFAULT_DB_ALIAS].copy()
        settings.DATABASES[db_name]['NAME'] = db_name

        try:
            # Verificar se o banco foi adicionado corretamente
            print(f"Configurando banco de dados para migração: {db_name}")
            call_command('migrate', database=db_name)  # Aplica as migrações no banco específico
            print(f"Migrações aplicadas com sucesso no banco {db_name}")
        except Exception as e:
            print(f"Erro ao aplicar migrações no banco {db_name}: {e}")

    @staticmethod
    def generate_confirmation_file(db_name, licenca):
        """
        Gera um arquivo de confirmação com os detalhes do banco de dados e da licença.
        """
        confirmation_data = {
            "db_name": db_name,
            "licenca_nome": licenca.lice_nome,
            "licenca_documento": licenca.lice_docu,
            "user": os.getenv("DB_USER", "postgres"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5433"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Define o caminho para o arquivo de confirmação
        confirmation_dir = "arquivos_confirmacao"
        os.makedirs(confirmation_dir, exist_ok=True)  # Cria o diretório, caso não exista
        file_path = os.path.join(confirmation_dir, f"confirmacao_{db_name}.txt")

        # Debug: imprime o caminho do arquivo
        print(f"Caminho do arquivo de confirmação: {file_path}")

        try:
            # Salva os dados em um arquivo de texto
            with open(file_path, 'w') as file:
                for key, value in confirmation_data.items():
                    file.write(f"{key}: {value}\n")
            print(f"Arquivo de confirmação gerado: {file_path}")
        except Exception as e:
            print(f"Erro ao gerar o arquivo de confirmação: {e}")

class DBRouter:
    """
    Roteador de banco de dados para ativar o banco correto da licença.
    """

    def db_for_read(self, model, **hints):
        return self.get_db()

    def db_for_write(self, model, **hints):
        return self.get_db()

    def get_db(self):
        """
        Obtém o banco de dados correto com base na sessão do usuário.
        """
        from django.contrib.sessions.models import Session
        from licencas.models import Licencas

        request = self.get_request()
        if request:
            licenca_id = request.session.get('licenca_id')
            if licenca_id:
                licenca = Licencas.objects.filter(id=licenca_id).first()
                if licenca:
                    return f'licenca_{licenca.documento}'  # Nome do banco

        return 'default'  # Se não houver licença, usa o banco padrão

    
    def get_user(self, user_id):
        from licencas.models import Usuarios 
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
