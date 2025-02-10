import json
import os
from django.conf import settings

def load_databases():
    """Carrega dinamicamente os bancos de dados do arquivo databases.json."""
    databases = {}

    try:
        with open(settings.DATABASES_FILE, "r") as f:
            databases = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️  Nenhum arquivo databases.json encontrado ou ele está corrompido.")

    return databases
