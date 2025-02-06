from django.db.models.signals import post_save
from django.dispatch import receiver
from licencas.models import Licencas
from licencas.db_router import LicenseDatabaseRouter

@receiver(post_save, sender=Licencas)
def criar_banco_automaticamente(sender, instance, created, **kwargs):
    """
    Quando uma nova licença é criada, criamos automaticamente o banco de dados correspondente.
    """
    if created:
        LicenseDatabaseRouter.ensure_database_exists(instance)
