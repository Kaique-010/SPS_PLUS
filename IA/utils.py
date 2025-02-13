import pandas as pd
from datetime import datetime, timedelta
from django.db import connection
from django.conf import settings
import os
import logging
logger = logging.getLogger(__name__)

def obter_dados_pedidos():

    banco_usuario = os.getenv('DB_USER')  

    data_inicio = (datetime.today() - timedelta(days=3000)).strftime('%Y-%m-%d')

    query = f"""
        SET search_path TO {banco_usuario};  -- Define o schema (banco) correto
        SELECT 
            p.pedi_nume AS pedido_id,
            p.pedi_data AS data_pedido,
            p.pedi_tota AS valor_total,
            p.pedi_clie AS cliente,
            e.enti_nome  AS cliente_nome,
            p.pedi_vend AS vendedor,
            i.item_prod AS produto_id,
            i.item_quan AS quantidade,
            i.item_suto AS valor_item
        FROM pedidospisos p
        JOIN itenspedidospisos i ON p.pedi_nume = i.item_pedi
        JOIN entidades e ON p.pedi_forn = e.enti_clie
        LEFT JOIN entidades v ON p.pedi_vend = e.enti_clie
        WHERE p.pedi_data >= '{data_inicio}'
        ORDER BY p.pedi_data DESC
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            colunas = [col[0] for col in cursor.description]
            dados = cursor.fetchall()
    except Exception as e:
        logger.error(f"Erro ao executar a consulta: {e}")
    return {"mensagem": "Erro ao recuperar dados."}


def gerar_insights():
    """Gera insights a partir dos pedidos e retorna dados prontos para JSON"""
    
    df = obter_dados_pedidos()

    if df.empty:
        return {"mensagem": "Nenhum dado disponível para análise."}

    insights = {}

    # Produto mais vendido
    produto_mais_vendido = df.groupby("produto_id")["quantidade"].sum().idxmax()
    insights["produto_mais_vendido"] = str(produto_mais_vendido)

    # Vendedor com maior faturamento
    vendedor_top = df.groupby("vendedor")["valor_total"].sum().idxmax()
    insights["vendedor_top"] = int(vendedor_top)

    # Cliente que mais comprou
    cliente_top = df.groupby("cliente")["valor_total"].sum().idxmax()
    insights["cliente_top"] = int(cliente_top)

    # Dia com mais vendas
    dia_mais_vendas = df.groupby("data_pedido")["valor_total"].sum().idxmax()
    insights["dia_mais_vendas"] = dia_mais_vendas.strftime("%Y-%m-%d")

    return insights