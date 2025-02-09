from datetime import date, timedelta
import json
from rest_framework import viewsets
from django.http import Http404
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import connection
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from Pedidos.models import  PedidoVenda, Itenspedidovenda
from .serializers import  PedidoVendaSerializer
from Pedidos.forms import ItensPedidoVendaForm, PedidoVendaForm, ItemPedidoFormSet
from produto.models import Produtos

class PedidoVendaViewSet(viewsets.ModelViewSet):
    queryset = PedidoVenda.objects.all()
    serializer_class = PedidoVendaSerializer


ItemPedidoFormSet = inlineformset_factory(PedidoVenda, Itenspedidovenda, fields=('iped_item', 'iped_prod', 'iped_quan', 'iped_unit'), extra=1, can_delete=True)

class PedidoVendaCreateView(CreateView):
    model = PedidoVenda
    form_class = PedidoVendaForm
    template_name = 'pedidocriar.html'
    success_url = reverse_lazy('pedidos_por_cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produtos.objects.all()

        if self.request.POST:
            context['formset'] = ItemPedidoFormSet(self.request.POST)
        else:
            context['formset'] = ItemPedidoFormSet(queryset=Itenspedidovenda.objects.none())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        print("Validando Form e Formset...")
        print(f"Form is valid: {form.is_valid()}")
        print(f"Formset is valid: {formset.is_valid()}")

        if form.is_valid() and formset.is_valid():
            pedido = form.save()  # Salva o pedido
            print(f"Pedido Salvo: {pedido}")

            # Obtém o último número de item dentro do pedido
            ultimo_item = Itenspedidovenda.objects.filter(iped_pedi=pedido).order_by('-iped_item').first()
            proximo_numero = (ultimo_item.iped_item + 1) if ultimo_item else 1

            itens = formset.save(commit=False)  # Evita salvar diretamente para modificar antes
            for idx, item in enumerate(itens, start=proximo_numero):
                item.iped_pedi = pedido  # Associa o pedido ao item
                item.iped_item = idx  # Define o número sequencial do item
                item.save()

                print(f"Item Salvo: {item}")  # Debug do item salvo

            messages.success(self.request, 'Pedido e itens salvos com sucesso!')
            return redirect(self.success_url)
        else:
            print("Erro no Formset:", formset.errors)
            messages.error(self.request, 'Erro ao salvar o pedido e os itens.')
            return self.form_invalid(form)

class PedidoVendaUpdateView(UpdateView):
    model = PedidoVenda
    form_class = PedidoVendaForm
    template_name = 'pedidocriar.html'
    success_url = reverse_lazy('pedidos_por_cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            # FormSet para POST (edição)
            context['formset'] = ItemPedidoFormSet(self.request.POST)
        else:
            # FormSet com itens existentes
            context['formset'] = ItemPedidoFormSet(queryset=Itenspedidovenda.objects.filter(iped_pedi=self.object))

        context['produtos'] = Produtos.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        print("Validando Form e Formset...")  # Log inicial
        print(f"Form is valid: {form.is_valid()}")
        print(f"Formset is valid: {formset.is_valid()}")

        if formset.is_valid():
            pedido = form.save()  # Salva o pedido
            print(f"Pedido Salvo: {pedido}")  # Debug do pedido salvo

            # Associa o pedido a cada item no formset e salva os itens
            for item_form in formset:
                item_form.instance.iped_pedi = pedido  # Associa o pedido ao item
                
                # Log para verificar cleaned_data
                print(f"Item form cleaned_data: {item_form.cleaned_data}")  # Verifique os dados limpos
                
                if item_form.cleaned_data:  # Verifique se os dados estão limpos e válidos
                    item_form.save()  # Salva o item
                    print(f"Item Salvo: {item_form.instance}")  # Debug do item salvo
                else:
                    print("Item não salvo, dados inválidos.")  # Log se o item não foi salvo

            messages.success(self.request, 'Pedido e itens salvos com sucesso!')
            return redirect(self.success_url)
        else:
            print("Erro no Formset:", formset.errors)  # Debug de erros do formset
            messages.error(self.request, 'Erro ao salvar o pedido e os itens.')
            return self.form_invalid(form)
        

class PedidoDetailView(DetailView):
    model = PedidoVenda
    template_name = 'pedido_detalhe.html'
    


class PedidoDeleteView(DeleteView):
    model = PedidoVenda
    template_name = 'pedido_excluir.html'
    success_url = reverse_lazy('pedidos_por_cliente')
    

def pedidos_por_cliente(request):
    nome_cliente = request.GET.get('nome_cliente', '')
    num_pedido = request.GET.get('num_pedido', '')
    page_number = request.GET.get('page', 1)

    query = """
    SELECT
        pedi_empr,
        pedi_fili,
        e.enti_nome AS nome_cliente,
        COUNT(DISTINCT pedi_nume) AS total_pedidos,
        ARRAY_AGG(pedi_nume) AS numeros_pedidos,
        ARRAY_AGG(pedi_data) AS datas_pedidos,
        SUM(pedi_tota) AS total_valor_pedidos,
        CASE 
            WHEN MAX(CAST(pedi_fina AS INTEGER)) = 0 THEN 'À VISTA'
            WHEN MAX(CAST(pedi_fina AS INTEGER)) = 1 THEN 'A prazo'
            WHEN MAX(CAST(pedi_fina AS INTEGER)) = 2 THEN 'SEM FINANCEIRO'
            ELSE 'Outro'
        END AS tipo_financeiro
    FROM pedidosvenda 
    LEFT JOIN entidades e ON pedi_forn = e.enti_clie AND pedi_empr = e.enti_empr
    WHERE 1=1
    """

    params = []

    if nome_cliente:
        query += " AND e.enti_nome LIKE %s"
        params.append(f'%{nome_cliente}%')

    if num_pedido:
        query += " AND pedi_nume = %s"
        params.append(num_pedido)

    query += """
        GROUP BY pedi_empr, pedi_fili, e.enti_nome
        ORDER BY total_pedidos DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        all_clientes_pedidos = dictfetchall(cursor)

    paginator = Paginator(all_clientes_pedidos, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'clientes_pedidos': page_obj,
        'nome_cliente': nome_cliente,
        'num_pedido': num_pedido,
        'page_obj': page_obj,
    }


    return render(request, 'pedidos_por_cliente.html', context)

def pedidos_necessitam_contato_view(request):
    hoje = date.today()
    dias_para_contato = 7  
    data_limite = hoje - timedelta(days=dias_para_contato)
    
    # Captura os filtros da requisição GET
    filtro_vendedor = request.GET.get('vendedor')
    filtro_pedido = request.GET.get('pedido_id')
    filtro_cliente = request.GET.get('cliente')

    # Ajusta a consulta SQL com base nos filtros
    query = """
        WITH UltimosPedidos AS (
            SELECT
                pedi_nume,
                e.enti_nome AS cliente,
                pedi_data,
                notas_contato,
                v.enti_nome AS vendedor,
                ROW_NUMBER() OVER (PARTITION BY e.enti_nome ORDER BY p.pedi_data DESC) AS rn
            FROM pedidosvenda p
            LEFT JOIN entidades e ON pedi_forn = e.enti_clie AND pedi_empr = e.enti_empr
            LEFT JOIN entidades v ON pedi_vend = v.enti_clie AND pedi_empr = v.enti_empr
        )
        SELECT
            pedi_nume,
            cliente,
            pedi_data,
            notas_contato,
            vendedor
        FROM UltimosPedidos
        WHERE rn = 1
        AND pedi_data <= %s
    """

    # Lista de parâmetros para a consulta
    params = [data_limite]

    # Aplica os filtros opcionais
    if filtro_vendedor:
        query += " AND vendedor = %s"
        params.append(filtro_vendedor)
    if filtro_pedido:
        query += " AND pedi_nume = %s"
        params.append(filtro_pedido)
    if filtro_cliente:
        query += " AND cliente = %s"
        params.append(filtro_cliente)

    query += " ORDER BY pedi_data DESC;"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        pedidos_necessitam_contato = dictfetchall(cursor)

    # Paginação
    paginator = Paginator(pedidos_necessitam_contato, 10)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    context = {
        'pedidos_necessitam_contato': page_obj,
        'filtro_vendedor': filtro_vendedor,
        'filtro_pedido': filtro_pedido,
        'filtro_cliente': filtro_cliente,
    }

    return render(request, 'pedidos_necessitam_contato.html', context)

def marcar_contato_realizado(request, pedido_id):
    try:
        pedido = PedidoVenda.objects.get(pedi_nume=pedido_id)
        pedido.contato_realizado = True
        pedido.data_contato = date.today()
        pedido.save()
    except PedidoVenda.DoesNotExist:
        return redirect('pedidos_necessitam_contato')
    except MultipleObjectsReturned:
        return redirect('pedidos_necessitam_contato')

    return redirect('detalhar_contato', pedido_id=pedido_id)

def detalhar_contato(request, pedido_id):
    query = """
        SELECT
            pedi_nume,
            e.enti_nome,
            e.enti_fone,
            e.enti_emai,
            e.enti_emai_empr,
            pedi_data,
            notas_contato
        FROM pedidosvenda
        LEFT JOIN entidades e ON pedi_forn = e.enti_clie AND pedi_empr = e.enti_empr
        WHERE pedi_nume = %s
    """
    
    params = [pedido_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultado = dictfetchall(cursor)

    if not resultado:
        raise Http404("Pedido não encontrado")

    pedido = resultado[0]

    if request.method == 'POST':
        notas = request.POST.get('notas')
        update_query = """
            UPDATE pedidosvenda
            SET notas_contato = %s
            WHERE pedi_nume = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_query, [notas, pedido_id])
        
        return redirect('pedidos_necessitam_contato')

    context = {
        'pedido': pedido,
    }

    return render(request, 'detalhar_contato.html', context)

def detalhar_cliente(request, pedido_id):
    query = """
        SELECT
            pedi_nume AS "Pedido",
            e.enti_nome AS "Nome Cliente",
            e.enti_fone AS "Telefone",
            e.enti_emai AS "Email1",
            e.enti_emai_empr AS "Email2",
            pedi_data AS "Data do Pedido",
            notas_contato AS "Notas"
        FROM pedidosvenda
        LEFT JOIN entidades e ON pedi_forn = e.enti_clie AND pedi_empr = e.enti_empr
        WHERE pedi_nume = %s
    """
    
    params = [pedido_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultado = dictfetchall(cursor)

    if not resultado:
        raise Http404("Pedido não encontrado")

    contato = resultado[0]

    if request.method == 'POST':
        notas = request.POST.get('notas')
        update_query = """
            UPDATE pedidosvenda
            SET notas_contato = %s
            WHERE pedi_nume = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_query, [notas, pedido_id])
        
        return redirect('crm_home')

    context = {
        'contato': contato,
    }

    return render(request, 'detalhar_cliente.html', context)


def dictfetchall(cursor):
    """Converte todas as linhas do cursor em um dicionário."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required
def dashboard(request):

    vendedor = request.GET.get('vendedor', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Obter lista de vendedores
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT e1.enti_clie, e1.enti_nome
            FROM pedidosvenda
            LEFT JOIN entidades e1 ON pedi_vend = e1.enti_clie AND pedi_empr = e1.enti_empr
            WHERE pedi_canc = false
            ORDER BY e1.enti_nome ASC;
        """)
        vendedores = cursor.fetchall()
        vendedores_list = [{'id': vendedor[0], 'nome': vendedor[1]} for vendedor in vendedores]

    # Consulta principal
    query = """
        SELECT 
            MAX(pedi_vend) AS "COD VENDEDOR",
            MAX(e1.enti_nome) AS "Nome Vendedor",
            COUNT(DISTINCT pedi_tota) AS "Total Pedidos",
            SUM(pedi_tota) AS "Total Valor dos Pedidos"
        FROM 
            pedidosvenda
       
        LEFT JOIN 
            entidades e1 ON pedi_vend = e1.enti_clie AND pedi_empr = e1.enti_empr
        WHERE 
            pedi_canc = false
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
        'vendedores': vendedores_list
    }

    return render(request, 'dashboard.html', context)












































































































































        

'''def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoVendaForm(request.POST)
        formset = ItemPedidoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)
            total = 0
            for item in formset:
                preco_unitario = item.cleaned_data.get('iped_unit')
                quantidade = item.cleaned_data.get('iped_quan')

                if preco_unitario and quantidade:
                    total += preco_unitario*quantidade
            pedido.save()
            return redirect('/pedidos/por-cliente/')

    else:
        form = PedidoVendaForm()
        formset = ItemPedidoFormSet()

    produtos = Produtos.objects.all()
    return render(request, 'pedidocriar.html', {
        'form': form,
        'formset': formset,
        'produtos': produtos,
    })'''

