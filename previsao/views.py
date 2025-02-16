from django.http import JsonResponse
from datetime import datetime
from .services import obter_dados_estoque, prever_saldo_futuro
from django.db import connections, router

def previsao_estoque(request, produto_id, empresa_id, filial_id, licenca_id):
    try:
        # 🔹 Coletamos os dados históricos, agora com o banco da licença
        df = obter_dados_estoque(produto_id, empresa_id, filial_id, licenca_id)

        # 🔎 Depuração: Verificar se o DataFrame tem os dados esperados
        print("Dados do DataFrame:")
        print(df)

        if df.empty:
            return JsonResponse({"error": "Sem dados para previsão"}, status=400)

        # 🔹 Aplicamos a previsão
        previsoes = prever_saldo_futuro(df)

        response = {
            "produto_id": produto_id,
            "empresa_id": empresa_id,
            "filial_id": filial_id,
            "previsoes": [{"data": data.strftime('%Y-%m-%d'), "saldo": round(float(saldo), 2)} for data, saldo in previsoes]
        }
        return JsonResponse(response)

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 🔍 Mostra o erro completo no terminal
        return JsonResponse({"error": str(e)}, status=500)
