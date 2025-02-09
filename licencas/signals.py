from django.db.models.signals import post_save
from django.dispatch import receiver
from licencas.models import Licencas
from licencas.db_router import LicenseDatabaseManager

@receiver(post_save, sender=Licencas)
def criar_banco_automaticamente(sender, instance, **kwargs):
    # Cria o banco de dados fora de qualquer transação
    LicenseDatabaseManager.ensure_database_exists(instance)
