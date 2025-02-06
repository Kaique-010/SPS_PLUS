# database_utils.py

from django.conf import settings
import json
import os

def load_databases():
    """Carrega os bancos de dados do arquivo JSON."""
    if not os.path.exists(settings.DATABASES_FILE):
        return {}

    try:
        with open(settings.DATABASES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  

def save_database(db_name):
    """Salva um novo banco de dados no arquivo JSON."""
    databases = load_databases()
    if db_name not in databases:
        databases[db_name] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db_name,
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "@spartacus201@"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5433"),
            "ATOMIC_REQUESTS": False,
        }
        with open(settings.DATABASES_FILE, "w") as file:
            json.dump(databases, file, indent=4)
