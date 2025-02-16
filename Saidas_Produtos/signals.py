from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Saidas_Produtos.models import SaidasEstoque
from produto.models import SaldoProduto

@receiver(post_save, sender=SaidasEstoque)
def update_saldo_on_saida(sender, instance, created, **kwargs):
    if created:
        produto_instance = instance.said_prod  # Acesso ao objeto do produto

        # Criar ou obter o saldo de produto associado à empresa e filial corretas
        saldo, _ = SaldoProduto.objects.get_or_create(
            sapr_prod=produto_instance,        # Relacionamento com o produto
            sapr_empr=instance.said_empr,      # Relacionamento com a empresa
            sapr_fili=instance.said_fili,      # Relacionamento com a filial
            defaults={'sapr_sald': 0}          # Se o saldo não existir, inicializa com 0
        )
        saldo.sapr_sald -= instance.said_tota  # Atualiza o saldo com a quantidade da saída
        saldo.save()

@receiver(post_delete, sender=SaidasEstoque)
def revert_saldo_on_saida_delete(sender, instance, **kwargs):
    try:
        produto_instance = instance.said_prod  # Acesso ao objeto do produto
        saldo = SaldoProduto.objects.get(sapr_prod=produto_instance)  # Acesse o saldo corretamente pelo código do produto
        saldo.saldo_estoque += instance.said_tota  # Reverte a quantidade no saldo
        saldo.save()
    except SaldoProduto.DoesNotExist:
        pass  # Se o saldo do produto não existir, não faz nada
