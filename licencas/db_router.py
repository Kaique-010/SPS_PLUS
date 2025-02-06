from licencas.middleware import get_current_request


class LicenseDatabaseRouter:
    def db_for_read(self, model, **hints):
        request = get_current_request()
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return request.user.licenca.lice_docu  # Usa o CPF/CNPJ como nome do banco
        return "default"  # Se não estiver autenticado, usa o banco padrão

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"  # Migrações só no banco padrão
