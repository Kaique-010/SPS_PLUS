import json
from django.conf import settings
from django.db import connections
from django.db import connection, OperationalError
from django.core.management import call_command
from threading import local
import psycopg2


class LicenseDatabaseManager:
    @staticmethod
    def ensure_database_exists(licenca):
        db_name = licenca.lice_nome
        if LicenseDatabaseManager.database_exists(db_name):
            print(f"Banco {db_name} já existe.")
            return

        LicenseDatabaseManager.create_database(db_name)
        LicenseDatabaseManager.apply_migrations_to_new_db(db_name)
        licenca.save()
        save_database(db_name)

    @staticmethod
    def database_exists(db_name):
        """Verifica se um banco já existe no PostgreSQL."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", [db_name])
                return cursor.fetchone() is not None
        except OperationalError:
            return False

    @staticmethod
    def create_database(db_name):
        """Cria um novo banco de dados no PostgreSQL fora de qualquer transação."""
        try:
            # Conexão direta ao PostgreSQL (sem transação)
            connection = psycopg2.connect(
                dbname='postgres',  # banco de dados default do PostgreSQL
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT']
            )
            connection.autocommit = True  # Necessário para criar o banco fora de transações
            cursor = connection.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Banco de dados {db_name} criado com sucesso!")
            cursor.close()
            connection.close()

            save_database(db_name)

        except Exception as e:
            print(f"Erro ao criar o banco {db_name}: {e}")

    @staticmethod
    def apply_migrations_to_new_db(db_name):
        """Aplica as migrações no banco recém-criado."""

        default_db = settings.DATABASES.get('default')
        if not default_db:
            raise KeyError("Configuração 'default' não encontrada em DATABASES.")

        # Adicionando a configuração para o novo banco de dados
        settings.DATABASES[db_name] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': default_db['USER'],
            'PASSWORD': default_db['PASSWORD'],
            'HOST': default_db['HOST'],
            'PORT': default_db['PORT'],
            'TIME_ZONE': 'America/Sao_Paulo',  
            'CONN_HEALTH_CHECKS': True,  
            'CONN_MAX_AGE': 600, 
            'AUTOCOMMIT': True,  
            'ATOMIC_REQUESTS': True,  
            'OPTIONS': {},  
        }

        # Forçando a recarga da configuração de banco de dados
        connections.databases[db_name] = settings.DATABASES[db_name]

        try:
            # Agora, podemos aplicar as migrações no banco recém-criado
            call_command('migrate', database=db_name)
            print(f"Migrações aplicadas no banco {db_name}")
        except Exception as e:
            print(f"Erro ao aplicar migrações no banco {db_name}: {e}")


def save_database(db_name):
    """
    Salva o nome do banco de dados no arquivo de configuração de bancos de dados JSON.
    """
    # Verifica se DATABASES já está carregado corretamente
    if settings.DATABASES is None:
        raise ValueError("As configurações de DATABASES não foram carregadas corretamente.")

    # Verifica se o banco já está presente
    databases = settings.DATABASES

    # Tentativa de carregar o arquivo JSON existente
    try:
        with open('databases.json', 'r') as f:
            databases = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # Se o arquivo não existir ou estiver vazio, inicializa como um dicionário vazio
        print("Arquivo 'databases.json' não encontrado ou corrompido. Criando novo arquivo.")
        databases = {}

    if db_name not in databases:
        databases[db_name] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': settings.DATABASES['default']['USER'],
            'PASSWORD': settings.DATABASES['default']['PASSWORD'],
            'HOST': settings.DATABASES['default']['HOST'],
            'PORT': settings.DATABASES['default']['PORT'],
            'TIME_ZONE': 'America/Sao_Paulo', 
            'CONN_HEALTH_CHECKS': True,  
            'CONN_MAX_AGE': 600, 
            'AUTOCOMMIT': True,  
            'ATOMIC_REQUESTS': True,  
            'OPTIONS': {},  
        }

       
        with open('databases.json', 'w') as f:
            json.dump(databases, f, indent=4)
    else:
        print(f"O banco {db_name} já está configurado.")