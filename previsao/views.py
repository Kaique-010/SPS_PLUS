from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from .services import obter_dados_estoque, prever_saldo_futuro
from django.db import connections, router
from django.core.cache import cache
import pandas as pd
import statsmodels.api as sm
from  produto.models import SaldoProduto, Produtos

def gerar_previsao(prod_codi, empresa, filial, dias_previsao, banco=None):
    cache_key = f"previsao_{prod_codi}_{empresa}_{filial}_{dias_previsao}"
    previsao = cache.get(cache_key)

    if previsao:
        return previsao


    query = SaldoProduto.objects.filter(
        sapr_prod__prod_codi=prod_codi,
        sapr_empr=empresa,
        sapr_fili=filial
    ).order_by("sapr_data")

    if banco:
        query = query.using(banco)

    if not query.exists():
        return None

    df = pd.DataFrame(list(query.values("sapr_data", "sapr_sald")))
    df["sapr_data"] = pd.to_datetime(df["sapr_data"])
    df.set_index("sapr_data", inplace=True)

    # Modelo SARIMA
    modelo = sm.tsa.statespace.SARIMAX(df["sapr_sald"], order=(1,1,1), seasonal_order=(1,1,1,7))
    resultado = modelo.fit()

    datas_futuras = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=dias_previsao)
    previsao_saldo = resultado.get_forecast(steps=dias_previsao).predicted_mean

    previsao = [{"data": data.strftime('%Y-%m-%d'), "saldo_previsto": saldo}
                for data, saldo in zip(datas_futuras, previsao_saldo)]
    
    cache.set(cache_key, previsao, timeout=86400)

    return previsao


def previsao_estoque(request, produto_id, empresa_id, filial_id, licenca_id):
    print("Licença na sessão:", request.session.get("licenca"))
    print("Banco ativo na sessão:", request.session.get("banco_ativo"))
    try:
        dias_previsao = 30  # Pode vir como parâmetro
        previsoes = gerar_previsao(produto_id, empresa_id, filial_id, dias_previsao)

        if not previsoes:
            return JsonResponse({"error": "Sem dados para previsão"}, status=400)

        response = {
            "produto_id": produto_id,
            "empresa_id": empresa_id,
            "filial_id": filial_id,
            "previsoes": previsoes
        }
        return JsonResponse(response)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)

def prever_saldo(request):
    produtos = Produtos.objects.all()
    previsao = []
    licenca = request.session.get("licenca")
    banco_ativo = request.session.get("banco_ativo")

    if not licenca or not banco_ativo:
        return render(request, "previsao/previsao_dashboard.html", {
            "produtos": produtos, "erro": "Erro ao obter licença e banco ativo!"
        })

    labels = []
    data = []

    if request.method == "POST":
        produto_id = request.POST.get("produto")
        empresa = request.POST.get("empresa")
        filial = request.POST.get("filial")
        dias_previsao = int(request.POST.get("dias", 30))

        previsao = gerar_previsao(produto_id, empresa, filial, dias_previsao, banco=banco_ativo)

        if not previsao:
            return render(request, "previsao/previsao_dashboard.html", {
                "produtos": produtos, "erro": "Sem dados para este produto, empresa e filial!"
            })

        labels = [p["data"] for p in previsao]
        data = [p["saldo_previsto"] for p in previsao]

    return render(request, "previsao/previsao_dashboard.html", {
        "produtos": produtos,
        "labels": labels,
        "data": data,
        "licenca": licenca,
        "banco_ativo": banco_ativo
    })
