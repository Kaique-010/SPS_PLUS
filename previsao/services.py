from django.db import connections, router
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from django.db.models import Sum
from Entradas_Produtos.models import EntradaEstoque
from Saidas_Produtos.models import SaidasEstoque
from produto.models import SaldoProduto

def obter_dados_estoque(produto_id, empresa_id, filial_id, licenca_id):
    """
    Obtém os dados históricos de entradas e saídas para um determinado produto.
    """
    try:
        # 🔹 Verifica o banco de dados correto com base na licença
        db_alias = router.db_for_read(licenca_id)  # Obtém o alias do banco baseado na licença
        with connections[db_alias].cursor() as cursor:  # Passa a conexão correta para a consulta
            # 🔹 Filtramos os dados históricos do produto na empresa e filial específicas
            entradas = EntradaEstoque.objects.using(db_alias).filter(
                entr_prod_id=produto_id, entr_empr=empresa_id, entr_fili=filial_id
            ).values('entr_data').annotate(quantidade=Sum('entr_quan'))

            saidas = SaidasEstoque.objects.using(db_alias).filter(
                said_prod_id=produto_id, said_empr=empresa_id, said_fili=filial_id
            ).values('said_data').annotate(quantidade=Sum('said_quan'))

            # 🔹 Pegamos o saldo atual do produto
            saldo_atual = SaldoProduto.objects.using(db_alias).filter(
                sapr_prod_id=produto_id, sapr_empr=empresa_id, sapr_fili=filial_id
            ).values_list('sapr_sald', flat=True).first() or 0

        # 🔹 Transformamos os dados em DataFrame para facilitar a análise
        df_entradas = pd.DataFrame(list(entradas)).rename(columns={'entr_data': 'data', 'quantidade': 'entrada'})
        df_saidas = pd.DataFrame(list(saidas)).rename(columns={'said_data': 'data', 'quantidade': 'saida'})

        # 🔹 Convertendo a coluna 'data' para datetime, caso não esteja nesse formato
        df_entradas['data'] = pd.to_datetime(df_entradas['data'])
        df_saidas['data'] = pd.to_datetime(df_saidas['data'])

        # 🔹 Unimos entradas e saídas em uma mesma tabela de datas
        df = pd.merge(df_entradas, df_saidas, on='data', how='outer').fillna(0)

        # 🔹 Ordenamos os dados por data
        df = df.sort_values('data')

        # 🔹 Criamos uma nova coluna de saldo acumulado
        df['saldo'] = saldo_atual + df['entrada'].cumsum() - df['saida'].cumsum()

        return df
    except Exception as e:
        print(f"Erro ao obter dados de estoque: {e}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro


def prever_saldo_futuro(df, dias=30):
    """
    Aplica Regressão Linear para prever o saldo futuro de um produto nos próximos 'dias' usando os dados do DataFrame.
    """
    if df.empty:
        return []

    try:
        # 🔹 Transformamos as datas em números sequenciais (dias)
        df['dias'] = (df['data'] - df['data'].min()).dt.days
        X = df[['dias']].values  # Variável independente (dias)
        y = df['saldo'].values   # Variável dependente (saldo)

        # 🔹 Criamos o modelo de Regressão Linear e treinamos com os dados históricos
        modelo = LinearRegression()
        modelo.fit(X, y)

        # 🔹 Criamos os próximos dias para previsão
        dias_futuros = np.arange(df['dias'].max() + 1, df['dias'].max() + dias + 1).reshape(-1, 1)
        previsoes = modelo.predict(dias_futuros)

        # 🔹 Retornamos as previsões com as datas futuras
        datas_futuras = [df['data'].max() + timedelta(days=int(d)) for d in dias_futuros.flatten()]
        return list(zip(datas_futuras, previsoes))
    except Exception as e:
        print(f"Erro ao prever saldo futuro: {e}")
        return []
