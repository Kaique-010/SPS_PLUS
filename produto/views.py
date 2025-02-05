from datetime import date, timedelta
import json
import csv
import os
from datetime import datetime 
from django.db.models import Sum
from django.db import connection, transaction
from django.db.models import OuterRef, Subquery
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.aggregates import ArrayAgg
from django.urls import reverse_lazy
from rest_framework import viewsets
from produto.serializers import ProdutosSerializers
from produto.models import Produtos, GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca, Tabelaprecos
from .forms import ProdutosForm, GrupoForm, SubgrupoForm, FamiliaForm, MarcaForm, TabelaprecosFormSet
from Entradas_Produtos.models import Entrada_Produtos
from Saidas_Produtos.models import Saida_Produtos
from produto.models import SaldoProduto
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializers
    filterset_fields = ['nome', 'id_produto']
    search_fields = ['nome', 'codigo_produto']
    

class ProdutoListView(ListView):
    model = Produtos
    template_name = 'produtos_lista.html'
    context_object_name = 'page_obj'
    paginate_by = 10  # Define o número de itens por página

    def get_queryset(self):
        """Filtra produtos com base em parâmetros de busca e inclui os preços associados."""
        nome = self.request.GET.get('nome', '')
        id_prod = self.request.GET.get('id_prod', '')

        # Subquery para buscar o saldo de cada produto
        saldo_subquery = SaldoProduto.objects.filter(
            produto_codigo=OuterRef('produto_codigo')
        ).values('saldo_estoque')[:1]

        # Base do queryset, agora com preços associados através de prefetch_related
        queryset = Produtos.objects.annotate(saldo_estoque=Subquery(saldo_subquery)).prefetch_related('tabelaprecos_set')

        # Aplicando filtros
        if nome:
            queryset = queryset.filter(nome_produto__icontains=nome)
        if id_prod:
            queryset = queryset.filter(produto_codigo=id_prod)

        return queryset.order_by('produto_codigo')
    

def produto_create(request):
    if request.method == 'POST':
        form = ProdutosForm(request.POST, request.FILES)
        formset = TabelaprecosFormSet(request.POST)  # Formset para a tabela de preços

        if form.is_valid() and formset.is_valid():
            cleaned_data = form.cleaned_data

            with transaction.atomic():
                # Gerar código do produto automaticamente, se não informado
                if not cleaned_data.get('produto_codigo'):
                    max_prod_codi = None
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT MAX(prod_codi) FROM produtos WHERE prod_empr = %s", [cleaned_data.get('prod_empr')])
                        max_prod_codi = cursor.fetchone()[0]
                        max_prod_codi = int(max_prod_codi) if max_prod_codi is not None else 0
                    
                    produto_codigo = max_prod_codi + 1
                    while Produtos.objects.filter(produto_codigo=produto_codigo).exists():
                        produto_codigo += 1
                    
                    cleaned_data['produto_codigo'] = str(produto_codigo)

                # Criar o novo produto
                novo_produto = Produtos.objects.create(
                    prod_empr=cleaned_data['prod_empr'],
                    produto_codigo=cleaned_data['produto_codigo'],
                    nome_produto=cleaned_data.get('nome_produto'),
                    unidade_medida=cleaned_data.get('unidade_medida'),
                    grupo=cleaned_data.get('grupo'),
                    subgrupo=cleaned_data.get('subgrupo'),
                    familia=cleaned_data.get('familia'),
                    local=cleaned_data.get('local'),
                    ncm=cleaned_data.get('ncm'),
                    marca=cleaned_data.get('marca'),
                    codigo_fabricante=cleaned_data.get('codigo_fabricante'),
                    foto=request.FILES.get('foto')
                )

                tabelaprecos_instances = formset.save(commit=False)
                for instance in tabelaprecos_instances:
                    instance.tabe_prod = novo_produto
                    instance.tabe_empr = novo_produto.prod_empr  # Atribuindo o valor de prod_empr para tabe_empr
                    instance.save()

                messages.success(request, f"Produto criado com sucesso! Código: {novo_produto.produto_codigo}")
                return redirect('produtos_lista.html')

    else:
        form = ProdutosForm()
        formset = TabelaprecosFormSet()

    return render(request, 'produtos_form.html', {'form': form, 'formset': formset})


def produto_update(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    
    if request.method == 'POST':
        form = ProdutosForm(request.POST, request.FILES, instance=produto)
        formset = TabelaprecosFormSet(request.POST, instance=produto)  # Carregar os preços para o produto

        if form.is_valid() and formset.is_valid():
            cleaned_data = form.cleaned_data
            
            with transaction.atomic():
                # Atualiza o produto
                produto = form.save()

                # Atualiza ou cria os preços associados ao produto
                tabelaprecos_instances = formset.save(commit=False)
                for instance in tabelaprecos_instances:
                    instance.tabe_prod = produto
                    instance.save()

                # Remover preços não enviados no formset
                tabelaprecos_ids = [instance.id for instance in tabelaprecos_instances]
                Tabelaprecos.objects.filter(tabe_prod=produto).exclude(id__in=tabelaprecos_ids).delete()

            messages.success(request, "Produto atualizado com sucesso!")
            return redirect('produtos_lista')  # Certifique-se de que o nome da URL esteja correto
    else:
        form = ProdutosForm(instance=produto)
        formset = TabelaprecosFormSet(queryset=Tabelaprecos.objects.filter(tabe_prod=produto))  # Preenche formset com preços existentes

    return render(request, 'produtos_form.html', {'form': form, 'formset': formset})



def produto_delete(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
        print(f"Produto: {produto.nome_produto} - Código: {produto.produto_codigo}")
        return redirect('produtos_lista.html')  
    return render(request, 'produto_confirm_delete.html', {'produto': produto})


class GrupoListView(ListView):
    model = GrupoProduto
    template_name = 'grupos_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class GrupoCreateView(CreateView):
    model = GrupoProduto
    form_class = GrupoForm
    template_name = 'grupo_create.html'
    success_url = reverse_lazy('grupos_list')

class GrupoUpdateView(UpdateView):
    model = GrupoProduto
    form_class = GrupoForm
    template_name = 'grupo_update.html'
    success_url = reverse_lazy('grupos_list')

class GrupoDeleteView(DeleteView):
    model = GrupoProduto
    template_name = 'grupo_delete.html'
    success_url = reverse_lazy('grupos_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grupo'] = self.object
        return context


class SubgrupoListView(ListView):
    model = SubgrupoProduto
    template_name = 'subgrupos_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class SubgrupoCreateView(CreateView):
    model = SubgrupoProduto
    form_class = SubgrupoForm
    template_name = 'subgrupo_create.html'
    success_url = reverse_lazy('subgrupos_list')

class SubgrupoUpdateView(UpdateView):
    model = SubgrupoProduto
    form_class = GrupoForm
    template_name = 'subgrupo_update.html'
    success_url = reverse_lazy('subgrupos_list')

class SubgrupoDeleteView(DeleteView):
    model = SubgrupoProduto
    template_name = 'subgrupo_delete.html'
    success_url = reverse_lazy('subgrupos_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subgrupo'] = self.object
        return context


# Views para Marca
class MarcaListView(ListView):
    model = Marca
    template_name = 'marcas_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'marca_create.html'
    success_url = reverse_lazy('marcas_list')

class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'marca_update.html'
    success_url = reverse_lazy('marcas_list')

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'marca_delete.html'
    success_url = reverse_lazy('marcas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca'] = self.object
        return context

# Views para FamiliaProduto
class FamiliaProdutoListView(ListView):
    model = FamiliaProduto
    template_name = 'familias_produto_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class FamiliaProdutoCreateView(CreateView):
    model = FamiliaProduto
    form_class = FamiliaForm
    template_name = 'familia_produto_create.html'
    success_url = reverse_lazy('familias_produto_list')

class FamiliaProdutoUpdateView(UpdateView):
    model = FamiliaProduto
    form_class = FamiliaForm
    template_name = 'familia_produto_update.html'
    success_url = reverse_lazy('familias_produto_list')

class FamiliaProdutoDeleteView(DeleteView):
    model = FamiliaProduto
    template_name = 'familia_produto_delete.html'
    success_url = reverse_lazy('familias_produto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familia_produto'] = self.object
        return context
    
    
def saldo(request):
    # Filtros de produto e período
    produto_selecionado = request.GET.get('produto', '')  
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    entradas = Entrada_Produtos.objects.all()
    saidas = Saida_Produtos.objects.all()

    # Filtro por produto
    if produto_selecionado:
        entradas = entradas.filter(produto_codigo=produto_selecionado)  # Use produto_codigo
        saidas = saidas.filter(produto_codigo=produto_selecionado)      # Use produto_codigo

    # Filtro por data
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        entradas = entradas.filter(criado__date__gte=data_inicio)
        saidas = saidas.filter(criado__date__gte=data_inicio)

    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        entradas = entradas.filter(criado__date__lte=data_fim)
        saidas = saidas.filter(criado__date__lte=data_fim)

    # Lista de produtos envolvidos
    produtos = list(set(
        [entrada.produto_codigo.nome_produto for entrada in entradas] +
        [saida.produto_codigo.nome_produto for saida in saidas]
    ))

    # Dados de entradas e saídas por produto
    entradas_data = [
        entradas.filter(produto_codigo__nome_produto=produto).aggregate(total=Sum('quantidade'))['total'] or 0
        for produto in produtos
    ]
    saidas_data = [
        saidas.filter(produto_codigo__nome_produto=produto).aggregate(total=Sum('quantidade'))['total'] or 0
        for produto in produtos
    ]

    # Saldo de cada produto
    saldos = {
        saldo.produto_codigo: float(saldo.saldo_estoque)  # Atualizando para usar produto_codigo
        for saldo in SaldoProduto.objects.all()
    }

    return render(request, 'saldos.html', {
        'produtos': SaldoProduto.objects.values_list('produto_codigo', flat=True).distinct(),
        'produtos_filtrados': produtos,
        'entradas_data': entradas_data,
        'saidas_data': saidas_data,
        'saldos': saldos,
        'produto_selecionado': produto_selecionado,
        'data_inicio': data_inicio.strftime('%Y-%m-%d') if data_inicio else '',
        'data_fim': data_fim.strftime('%Y-%m-%d') if data_fim else '',
    })



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def exportar_produtos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Código Produto', 'Nome', 'Unidade Medida', 'Código Grupo', 'Descrição Grupo', 
        'Código Subgrupo', 'Descrição Subgrupo', 'Código Família', 'Descrição Família', 
        'Local', 'NCM', 'Código Marca', 'Nome Marca', 'Código Fabricante', 
        'Preço Custo', 'Preço à Vista', 'Preço a Prazo', 'Saldo Estoque'
    ])

    # Montagem da query SQL
    query = """
    SELECT DISTINCT 
        s.sapr_empr AS "Empresa",
        s.sapr_fili AS "Filial",
        p.prod_codi AS "codigo_produto",
        p.prod_nome AS "nome_produto",
        p.prod_unme AS "unidade_medida",
        p.prod_grup AS "codigo_grupo",
        gp.grup_desc AS "descricao_grupo",
        p.prod_sugr AS "codigo_subgrupo",
        sp.sugr_desc AS "descricao_subgrupo",
        p.prod_fami AS "codigo_familia",
        fp.fami_desc AS "descricao_familia",
        p.prod_loca AS "local",
        p.prod_ncm AS "ncm",
        p.prod_marc AS "codigo_marca",
        p.prod_foto AS "foto",
        m.marc_nome AS "nome_marca",
        p.prod_codi_fabr AS "codigo_fabricante",
        t.tabe_cuge AS "preco_custo",
        t.tabe_avis AS "preco_a_vista",
        t.tabe_apra AS "preco_a_prazo",
        s.sapr_sald AS "saldo_estoque"
    FROM 
        produtos p
    LEFT JOIN 
        tabelaprecos t ON p.prod_codi::text = t.tabe_prod::text
    LEFT JOIN 
        gruposprodutos gp ON p.prod_grup::text = gp.grup_codi::text
    LEFT JOIN 
        subgruposprodutos sp ON p.prod_sugr::text = sp.sugr_codi::text
    LEFT JOIN 
        familiaprodutos fp ON p.prod_fami::text = fp.fami_codi::text
    LEFT JOIN 
        saldosprodutos s ON p.prod_codi::text = s.sapr_prod::text
    LEFT JOIN 
        marca m ON p.prod_marc = m.marc_codi
    WHERE 
        s.sapr_sald > 0
        
        AND s.sapr_fili >= 0
    """


    with connection.cursor() as cursor:
        cursor.execute(query)
        produtos = dictfetchall(cursor)

   
    if produtos:
        print("Colunas disponíveis:", produtos[0].keys())

 
    for produto in produtos:
        writer.writerow([
            produto.get('codigo_produto', ''),
            produto.get('nome_produto', ''),
            produto.get('unidade_medida', ''),
            produto.get('codigo_grupo', ''),
            produto.get('descricao_grupo', ''),
            produto.get('codigo_subgrupo', ''),
            produto.get('descricao_subgrupo', ''),
            produto.get('codigo_familia', ''),
            produto.get('descricao_familia', ''),
            produto.get('local', ''),  
            produto.get('ncm', ''),
            produto.get('codigo_marca', ''),
            produto.get('nome_marca', ''),
            produto.get('codigo_fabricante', ''),
            produto.get('preco_custo', ''),
            produto.get('preco_a_vista', ''),
            produto.get('preco_a_prazo', ''),
            produto.get('saldo_estoque', '')
        ])

    return response

def dictfetchall(cursor):
    "Converte os resultados da consulta para uma lista de dicionários."
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]