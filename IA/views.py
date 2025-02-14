import logging
from django.http import JsonResponse
from IA.utils import gerar_insights  # Certifique-se de que a função está corretamente importada

# Configuração do logger
logger = logging.getLogger(__name__)

def obter_insights(request):
    try:
        logger.info("Iniciando o processo de obtenção dos insights.")
        
        # Agora passando request corretamente
        insights = gerar_insights(request)
        
        logger.info(f"Insights obtidos com sucesso: {insights}")

        # Retornando os insights em formato JSON
        return JsonResponse(insights)

    except Exception as e:
        # Logando a exceção para entender onde o erro ocorre
        logger.error(f"Erro ao obter os insights: {str(e)}")
        
        # Retornando a mensagem de erro no formato JSON
        return JsonResponse({'error': str(e)}, status=500)
