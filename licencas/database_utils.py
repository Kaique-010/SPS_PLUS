# database_utils.py

from django.conf import settings
import json
import os

def load_databases():
    """Carrega as configurações de banco de dados a partir de um arquivo JSON."""
    try:
        with open('databases.json', 'r') as f:
            databases = json.load(f)
            settings.DATABASES = databases  # Atualiza as configurações de DATABASES
            print(f"Bancos de dados carregados com sucesso: {settings.DATABASES}")
    except FileNotFoundError:
        print("Arquivo de bancos de dados não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON de bancos de dados.")

'''def save_database(db_name):
    """
    Salva o nome do banco de dados no arquivo de configuração de bancos de dados JSON.
    """
    if settings.DATABASES is None:
        raise ValueError("As configurações de DATABASES não foram carregadas corretamente.")
    
    # Verifica se o banco já está presente
    databases = settings.DATABASES

    if db_name not in databases:
        databases[db_name] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': settings.DATABASES['default']['USER'],
            'PASSWORD': settings.DATABASES['default']['PASSWORD'],
            'HOST': settings.DATABASES['default']['HOST'],
            'PORT': settings.DATABASES['default']['PORT'],
        }
        # Salva as configurações atualizadas no arquivo JSON
        with open('databases.json', 'w') as f:
            json.dump(databases, f, indent=4)
    else:
        print(f"O banco {db_name} já está configurado.")
'''