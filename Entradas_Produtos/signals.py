from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Entradas_Produtos.models import EntradaEstoque
from produto.models import SaldoProduto

@receiver(post_save, sender=EntradaEstoque)
def update_saldo_on_entrada(sender, instance, created, **kwargs):
    if created:
        produto_instance = instance.entr_prod  # Acesso direto ao objeto do produto

        # Criar ou obter o saldo de produto associado à empresa e filial corretas
        saldo, _ = SaldoProduto.objects.get_or_create(
            sapr_prod=produto_instance,        # Relacionamento com o produto
            sapr_empr=instance.entr_empr,      # Relacionamento com a empresa
            sapr_fili=instance.entr_fili,      # Relacionamento com a filial
            defaults={'sapr_sald': 0}          # Se o saldo não existir, inicializa com 0
        )
        saldo.sapr_sald += instance.entr_tota  # Atualiza o saldo com a quantidade da entrada
        saldo.save()

@receiver(post_delete, sender=EntradaEstoque)
def revert_saldo_on_entrada_delete(sender, instance, **kwargs):
    try:
        produto_instance = instance.entr_prod  # Acesso ao objeto do produto
        saldo = SaldoProduto.objects.get(sapr_prod=produto_instance)  # Acesse o saldo corretamente pelo código do produto
        saldo.saldo_estoque -= instance.entr_tota  # Reverte a quantidade no saldo
        saldo.save()
    except SaldoProduto.DoesNotExist:
        pass  # Se o saldo do produto não existir, não faz nada
