import json

class LicenseMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar as configurações dos bancos de dados do arquivo JSON
        with open('./databases.json') as f:
            self.database_configs = json.load(f)

    def set_database(self, license_name):
        if license_name in self.database_configs:
            db_config = self.database_configs[license_name]
           