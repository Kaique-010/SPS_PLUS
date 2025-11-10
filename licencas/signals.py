from django.db.models.signals import post_save
from django.dispatch import receiver
from licencas.models import Licencas

# Removido: criação automática de banco via JSON/config antiga.
# Mantemos o sinal vazio para futuras integrações, se necessário.
@receiver(post_save, sender=Licencas)
def criar_banco_automaticamente(sender, instance, **kwargs):
    return
