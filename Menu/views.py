import json
from django.shortcuts import render
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db import connection

from licencas.models import Licencas


def dictfetchall(cursor):
    """Converte o resultado do cursor em uma lista de dicionários."""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required
def home(request):
    licenca= Licencas.objects.all()
    user = get_user(request)  # Obtém o usuário autenticado
    print(f"Usuário autenticado na home? {user.is_authenticated}")
    print(f"Usuário: {user}")  # Verifica se o usuário está correto
    print(f"Session Key: {request.session.session_key}")
    print(f"Licença: {Licencas.lice_nome}")
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
        data = dictfetchall(cursor)

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
        'user': user
    }

    return render(request, 'home.html', context)


