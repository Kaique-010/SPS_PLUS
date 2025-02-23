from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
import json

@login_required
def home(request):
    licenca_nome = request.session.get("licenca_lice_nome")
    print(f"Licença na home: {licenca_nome}")
    db_config = request.session.get("db_config")  
    print(f"DB Config na home: {db_config}")
    usuario = request.user  # Obtém o usuário autenticado
    print(f"Usuário autenticado na home? {usuario.is_authenticated}")

    vendedor = request.GET.get('vendedor', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Obter lista de vendedores
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT e1.enti_clie, e1.enti_nome
            FROM pedidosvenda 
            LEFT JOIN entidades e1 ON pedi_vend = e1.enti_clie AND pedi_empr = e1.enti_empr
            WHERE pedi_canc = false  -- Certifique-se de filtrar pedidos cancelados
            ORDER BY e1.enti_nome ASC;
        """)
        vendedores = cursor.fetchall()
        vendedores_list = [{'id': vendedor[0], 'nome': vendedor[1]} for vendedor in vendedores]

    # Consulta principal
    query = """
        SELECT 
            MAX(pedi_vend) AS "COD VENDEDOR",
            MAX(e1.enti_nome) AS "Nome Vendedor",
            COUNT(DISTINCT pedi_nume) AS "Total Pedidos",  -- Ajuste aqui
            SUM(pedi_tota) AS "Total Valor dos Pedidos"
        FROM 
            pedidosvenda
        LEFT JOIN 
            entidades e1 ON pedi_vend = e1.enti_clie AND pedi_empr = e1.enti_empr
        WHERE 
            pedi_canc = false  -- Filtrar pedidos cancelados
    """

    params = []
    if vendedor:
        query += " AND e1.enti_clie = %s"
        params.append(vendedor)

    if data_inicio:
        query += " AND pedi_data >= %s"
        params.append(data_inicio)

    if data_fim:
        query += " AND pedi_data <= %s"
        params.append(data_fim)

    query += """
        GROUP BY 
            pedi_vend, e1.enti_nome
        ORDER BY 
            e1.enti_nome ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = dictfetchall(cursor)  # Usa a função dictfetchall para converter o resultado

    # Prepare data for the chart
    labels = [item['Nome Vendedor'] for item in data]
    total_pedidos = [float(item['Total Pedidos']) for item in data]
    total_valor_pedido = [float(item['Total Valor dos Pedidos']) for item in data]

    context = {
        'labels': json.dumps(labels),
        'total_pedidos': json.dumps(total_pedidos),
        'total_valor_pedido': json.dumps(total_valor_pedido),
        'vendedor': vendedor,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'vendedores': vendedores_list,
        'usuario': usuario
    }

    return render(request, 'home.html', context)

def dictfetchall(cursor):
    """
    Retorna todas as linhas de um cursor como uma lista de dicionários.
    """
    columns = [col[0] for col in cursor.description]  # Obtém os nomes das colunas
    return [
        dict(zip(columns, row))  # Converte cada linha em um dicionário
        for row in cursor.fetchall()
    ]