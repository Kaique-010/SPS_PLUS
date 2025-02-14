import pandas as pd
from datetime import datetime, timedelta
from django.db import connections
import logging

logger = logging.getLogger(__name__)

def obter_insight_vendas(request):
    banco_usuario = request.session.get('banco_usuario') or request.session.get('licenca_nome')

    if not banco_usuario:
        logger.error("Banco de dados do usuário não encontrado na sessão!")
        return {}

    logger.info(f"🎯 Utilizando banco de dados: {banco_usuario}")

    data_inicio = (datetime.today() - timedelta(days=3000)).strftime('%Y-%m-%d')

    query_vendas = f"""
        SELECT 
            pr.prod_nome AS nome_produto,
            SUM(i.item_quan) AS quantidade_vendida,
            SUM(p.pedi_tota) AS total_venda,
            p.pedi_vend AS vendedor,
            p.pedi_clie AS cliente,
            p.pedi_data AS data_pedido
        FROM {banco_usuario}.public.pedidospisos p
        JOIN {banco_usuario}.public.itenspedidospisos i ON p.pedi_nume = i.item_pedi
        JOIN {banco_usuario}.public.produtos pr ON pr.prod_codi = i.item_prod
        WHERE p.pedi_data >= '{data_inicio}'
        GROUP BY pr.prod_nome, p.pedi_vend, p.pedi_clie, p.pedi_data
        ORDER BY total_venda DESC
        LIMIT 1;
    """

    try:
        with connections[banco_usuario].cursor() as cursor:
            cursor.execute(query_vendas)
            colunas = [col[0] for col in cursor.description]
            dados = cursor.fetchall()
            if dados:
                return {
                    "produto_mais_vendido": dados[0][0],
                    "quantidade_produto": dados[0][1],
                    "vendedor_top": dados[0][3],
                    "cliente_top": dados[0][4],
                    "dia_mais_vendas": dados[0][5].strftime('%Y-%m-%d')
                }
            return {}
    except Exception as e:
        logger.error(f"Erro ao executar a consulta de vendas: {e}")
        return {}


def obter_insight_estoque(request):
    banco_usuario = request.session.get('banco_usuario') or request.session.get('licenca_nome')

    if not banco_usuario:
        logger.error("Banco de dados do usuário não encontrado na sessão!")
        return {}

    logger.info(f"🎯 Utilizando banco de dados: {banco_usuario}")

    query_estoque = f"""
       SELECT 
        p.prod_codi AS "codigo_produto",
        p.prod_nome AS "nome_produto",
        p.prod_unme AS "unidade_medida",
        gp.grup_desc AS "descricao_grupo",
        fp.fami_desc AS "descricao_familia",
        m.marc_nome AS "nome_marca",
        s.sapr_sald AS "saldo_estoque",
        (SELECT SUM(sapr_sald) FROM saldosprodutos) AS "estoque_total"
    FROM 
        produtos p
    LEFT JOIN 
        gruposprodutos gp ON p.prod_grup::text = gp.grup_codi::text
    LEFT JOIN 
        familiaprodutos fp ON p.prod_fami::text = fp.fami_codi::text
    LEFT JOIN 
        saldosprodutos s ON p.prod_codi::text = s.sapr_prod::text
    LEFT JOIN 
        marca m ON p.prod_marc = m.marc_codi
    WHERE 
        s.sapr_sald > 0
    ORDER BY 
        s.sapr_sald ASC 
    LIMIT 1
    """

    try:
        with connections[banco_usuario].cursor() as cursor:
            cursor.execute(query_estoque)
            colunas = [col[0] for col in cursor.description]
            dados = cursor.fetchone()
            if dados:
                return {
                    "produto_menor_estoque": {
                        "codigo": dados[0],
                        "nome": dados[1],
                        "unidade": dados[2],
                        "grupo": dados[3],
                        "familia": dados[4],
                        "marca": dados[5],
                        "saldo": dados[6]
                    },
                    "estoque_total": dados[7] if dados[7] else 0
                }
            return {}
    except Exception as e:
        logger.error(f"Erro ao executar a consulta de estoque: {e}")
        return {}


def obter_insight_clientes_inativos(request):
    banco_usuario = request.session.get('banco_usuario') or request.session.get('licenca_nome')

    if not banco_usuario:
        logger.error("Banco de dados do usuário não encontrado na sessão!")
        return {}

    logger.info(f"🎯 Utilizando banco de dados: {banco_usuario}")

    # Data limite: Clientes que não compram há mais de 6 meses
    data_limite = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')

    query_clientes_inativos = f"""
        WITH UltimosPedidos AS (
            SELECT
                p.pedi_nume AS numero_pedido,
                e.enti_nome AS cliente,
                p.pedi_data AS data_ultima_compra,
                v.enti_nome AS vendedor,
                ROW_NUMBER() OVER (PARTITION BY e.enti_nome ORDER BY p.pedi_data DESC) AS rn
            FROM pedidospisos p
            LEFT JOIN entidades e ON p.pedi_clie = e.enti_clie AND p.pedi_empr = e.enti_empr
            LEFT JOIN entidades v ON p.pedi_vend = v.enti_clie AND p.pedi_empr = v.enti_empr
        )
        SELECT
            cliente,
            data_ultima_compra,
            vendedor
        FROM UltimosPedidos
        WHERE rn = 1
        AND data_ultima_compra <= %s
    """

    try:
        with connections[banco_usuario].cursor() as cursor:
            cursor.execute(query_clientes_inativos, [data_limite])
            colunas = [col[0] for col in cursor.description]
            dados = cursor.fetchall()
            if dados:
                clientes_inativos = [
                    {"cliente": linha[0], "data_ultima_compra": linha[1], "vendedor": linha[2]}
                    for linha in dados
                ]
                return {"clientes_inativos": clientes_inativos}
            return {}
    except Exception as e:
        logger.error(f"Erro ao executar a consulta de clientes inativos: {e}")
        return {}



def obter_insight_contato_aniversario(request):
    banco_usuario = request.session.get('banco_usuario') or request.session.get('licenca_nome')

    if not banco_usuario:
        logger.error("Banco de dados do usuário não encontrado na sessão!")
        return {}

    logger.info(f"🎯 Utilizando banco de dados: {banco_usuario}")

    data_atual = datetime.now().strftime('%Y-%m-%d')

    query_aniversario = f"""
        SELECT COUNT(*) AS clientes_aniversario
        FROM {banco_usuario}.public.entidades e
        WHERE EXTRACT(MONTH FROM e.enti_data_part) = EXTRACT(MONTH FROM CURRENT_DATE)
    """

    try:
        with connections[banco_usuario].cursor() as cursor:
            cursor.execute(query_aniversario)
            dados = cursor.fetchall()
            if dados:
                return {
                    "clientes_aniversario": dados[0][0]
                }
            return {}
    except Exception as e:
        logger.error(f"Erro ao executar a consulta de aniversários: {e}")
        return {}





def gerar_insights(request):
    insights = {}
    # Chamar as funções de cada insight
    vendas = obter_insight_vendas(request)
    estoque = obter_insight_estoque(request)
    clientes_inativos = obter_insight_clientes_inativos(request)
    contato_aniversario = obter_insight_contato_aniversario(request)

    # Unir os dados
    insights.update(vendas)
    insights.update(estoque)
    insights.update(clientes_inativos)
    insights.update(contato_aniversario)

    if not insights:
        return {"mensagem": "Nenhum dado disponível para análise."}

    return insights
