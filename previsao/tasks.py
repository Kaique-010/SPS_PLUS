

from celery import shared_task
from produto.models import SaldoProduto
from .views import prever_saldo

@shared_task
def calcular_previsao_periodica(prod_codi, empresa, filial, dias_previsao):
    # Chama a função de previsão, que agora usa cache
    previsao = prever_saldo(prod_codi, empresa, filial, dias_previsao)
    
    # Aqui você pode adicionar a lógica para armazenar previsões no banco ou enviar e-mails
    if previsao:
        # Exemplo: salvar previsões no banco ou enviar e-mail
        print(f"Previsão calculada para o produto {prod_codi}: {previsao}")
    return previsao
