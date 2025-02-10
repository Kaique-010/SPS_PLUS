from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Saidas_Produtos.models import Saida_Produtos
from produto.models import SaldoProduto


@receiver(post_save, sender=Saida_Produtos)
def update_saldo_on_entrada(sender, instance, created, **kwargs):
    if created:
        # Obtenha a instância do produto
        produto_instance = instance.prod_codi  

        saldo, _ = SaldoProduto.objects.get_or_create(
            prod_codi=produto_instance,  # Atribua a instância aqui
            defaults={'empresa': '', 'filial': '', 'saldo_estoque': 0}
        )
        saldo.saldo_estoque -= instance.quantidade
        saldo.save()



@receiver(post_delete, sender=Saida_Produtos)
def revert_saldo_on_entrada_delete(sender, instance, **kwargs):
    try:
        produto_instance = instance.prod_codi  # Obtenha a instância do produto
        saldo = SaldoProduto.objects.get(prod_codi=produto_instance)  # Use a instância aqui
        saldo.saldo_estoque += instance.quantidade
        saldo.save()
    except SaldoProduto.DoesNotExist:
        pass