'''from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PedidoVenda, Itenspedidovenda

@receiver(post_save, sender=PedidoVenda)
def salvar_itens_pedido(sender, instance, created, **kwargs):
    if created and hasattr(instance, '_itens'):
        print(f"Itens recebidos: {instance._itens}")
        for item_data in instance._itens:
            try:
                Itenspedidovenda.objects.create(
                    iped_pedi=instance,
                    iped_unit=item_data.get('iped_unit'),
                    iped_quan=item_data.get('iped_quan'),
                    iped_prod=item_data.get('iped_prod'),
                    iped_empr=instance.pedi_empr,
                    iped_fili=instance.pedi_fili,
                    iped_item=item_data.get('iped_item'),
                )
            except Exception as e:
                print(f"Erro ao salvar item: {item_data}, erro: {e}", flush=True)
    else:
        print(f"Pedido {instance} salvo sem itens.", flush=True)
        print(f"Dados do pedido: {instance}")
        print(f"Itens recebidos: {instance._itens}")

'''