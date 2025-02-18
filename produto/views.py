from datetime import date, timedelta
from decimal import Decimal
import decimal
import json
import csv
import os
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Sum
from django.db import connection, transaction
from django.db.models import OuterRef, Subquery
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.aggregates import ArrayAgg
from django.urls import reverse_lazy
from rest_framework import viewsets
from licencas.mixins import LicenseMixin
from produto.serializers import ProdutosSerializers
from produto.models import Produtos, GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca, Tabelaprecos
from .forms import ProdutosForm, GrupoForm, SubgrupoForm, FamiliaForm, MarcaForm, TabelaprecosFormSet
from Entradas_Produtos.models import EntradaEstoque
from Saidas_Produtos.models import SaidasEstoque
from produto.models import SaldoProduto
from django.views.generic import DeleteView, ListView, CreateView, UpdateView

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializers
    filterset_fields = ['nome_produto', 'prod_codi']
    search_fields = ['nome_produto', 'prod_codi']
class ProdutoListView(LicenseMixin, ListView):
    model = Produtos
    template_name = 'produtos_lista.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        
        nome = self.request.GET.get('nome_produto', '')
        id_prod = self.request.GET.get('prod_codi', '')

        # Tenta converter o valor de id_prod para número
        if id_prod:
            try:
                id_prod = int(id_prod)
            except ValueError:
                id_prod = None  # Se não for numérico, define como None

        # Consulta para obter o saldo de cada produto (usando o banco de dados da licença)
        saldo_produtos = SaldoProduto.objects.using(db_name).all()
        if id_prod:
            saldo_produtos = saldo_produtos.filter(sapr_prod__prod_codi=id_prod)

        # Subquery para adicionar o saldo no queryset de Produtos (usando o banco de dados da licença)
        produtos = Produtos.objects.using(db_name).all()
        if nome:
            produtos = produtos.filter(prod_nome__icontains=nome)

        # Usando o saldo de produtos para adicionar à consulta principal
        produtos_com_saldo = produtos.annotate(
            saldo=Subquery(saldo_produtos.filter(sapr_prod=OuterRef('prod_codi')).values('sapr_sald')[:1])
        )

        return produtos_com_saldo.order_by('prod_codi')




class ProdutoCreateView(LicenseMixin, CreateView):
    model = Produtos
    form_class = ProdutosForm
    template_name = 'produtos_form.html'

    def form_valid(self, form):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        formset = TabelaprecosFormSet(self.request.POST)
        if form.is_valid() and formset.is_valid():
            cleaned_data = form.cleaned_data
            
            with transaction.atomic():
                if not cleaned_data.get('prod_codi'):
                    max_prod_codi = None
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT MAX(prod_codi) FROM produtos WHERE prod_empr = %s", [cleaned_data.get('prod_empr')])
                        max_prod_codi = cursor.fetchone()[0] or 0
                    
                    produto_codigo = max_prod_codi + 1
                    while Produtos.objects.filter(prod_codi=produto_codigo).exists():
                        produto_codigo += 1
                    
                    cleaned_data['prod_codi'] = str(produto_codigo)

                novo_produto = form.save(commit=False)                
                novo_produto.save(using=db_name)

                tabelaprecos_instances = formset.save(commit=False)
                for instance in tabelaprecos_instances:
                    instance.tabe_prod = novo_produto
                    instance.tabe_empr = novo_produto.prod_empr
                    instance.save()

                messages.success(self.request, f"Produto criado com sucesso! Código: {novo_produto.prod_codi}")
                return redirect('produtos_lista')
        
        return self.form_invalid(form)



class ProdutoUpdateView(LicenseMixin, UpdateView):
    model = Produtos
    form_class = ProdutosForm
    template_name = 'produtos_update.html'

    def get_object(self, queryset=None):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        prod_codi = self.kwargs.get("prod_codi")

        print(f"[DEBUG] Buscando produto  com prod_codi={prod_codi} no banco {db_name}")

        produtos= Produtos.objects.using(db_name).filter(prod_codi=prod_codi).first()
        
        if not produtos:
            raise Http404("Entidade não encontrada.")
        
        return produtos

    def form_valid(self, form):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"

        formset = TabelaprecosFormSet(self.request.POST, instance=self.object, queryset=Tabelaprecos.objects.using(db_name).filter(tabe_prod=self.object))

        if form.is_valid() and formset.is_valid():
            with transaction.atomic(using=db_name):
                produto = form.save(commit=False)
                produto.save(using=db_name)

                tabelaprecos_instances = formset.save(commit=False)
                for instance in tabelaprecos_instances:
                    instance.tabe_prod = produto
                    instance.save(using=db_name)

                tabelaprecos_ids = [instance.id for instance in tabelaprecos_instances]
                Tabelaprecos.objects.using(db_name).filter(tabe_prod=produto).exclude(id__in=tabelaprecos_ids).delete()

            messages.success(self.request, "Produto atualizado com sucesso!")
            return redirect('produtos_lista')

        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        
        context['formset'] = TabelaprecosFormSet(instance=self.object, queryset=Tabelaprecos.objects.using(db_name).filter(tabe_prod=self.object))
        
        return context

class ProdutoDeleteView(LicenseMixin, DeleteView):
    model = Produtos
    template_name = 'produto_confirm_delete.html'
    success_url = reverse_lazy('produtos_lista')

    def delete(self, request, *args, **kwargs):
        produto = self.get_object()
        messages.success(self.request, f"Produto excluído com sucesso! Código: {produto.prod_codi}")
        return super().delete(request, *args, **kwargs)

class GrupoListView(LicenseMixin, ListView):
    model = GrupoProduto
    template_name = 'grupos_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class GrupoCreateView(LicenseMixin, CreateView):
    model = GrupoProduto
    form_class = GrupoForm
    template_name = 'grupo_create.html'
    success_url = reverse_lazy('grupos_list')

class GrupoUpdateView(LicenseMixin, UpdateView):
    model = GrupoProduto
    form_class = GrupoForm
    template_name = 'grupo_update.html'
    success_url = reverse_lazy('grupos_list')

class GrupoDeleteView(LicenseMixin, DeleteView):
    model = GrupoProduto
    template_name = 'grupo_delete.html'
    success_url = reverse_lazy('grupos_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grupo'] = self.object
        return context

class SubgrupoListView(LicenseMixin, ListView):
    model = SubgrupoProduto
    template_name = 'subgrupos_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class SubgrupoCreateView(LicenseMixin, CreateView):
    model = SubgrupoProduto
    form_class = SubgrupoForm
    template_name = 'subgrupo_create.html'
    success_url = reverse_lazy('subgrupos_list')

class SubgrupoUpdateView(LicenseMixin, UpdateView):
    model = SubgrupoProduto
    form_class = GrupoForm
    template_name = 'subgrupo_update.html'
    success_url = reverse_lazy('subgrupos_list')

class SubgrupoDeleteView(LicenseMixin, DeleteView):
    model = SubgrupoProduto
    template_name = 'subgrupo_delete.html'
    success_url = reverse_lazy('subgrupos_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subgrupo'] = self.object
        return context

# Views para Marca
class MarcaListView(LicenseMixin, ListView):
    model = Marca
    template_name = 'marcas_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class MarcaCreateView(LicenseMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'marca_create.html'
    success_url = reverse_lazy('marcas_list')

class MarcaUpdateView(LicenseMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'marca_update.html'
    success_url = reverse_lazy('marcas_list')

class MarcaDeleteView(LicenseMixin, DeleteView):
    model = Marca
    template_name = 'marca_delete.html'
    success_url = reverse_lazy('marcas_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marca'] = self.object
        return context

# Views para FamiliaProduto
class FamiliaProdutoListView(LicenseMixin, ListView):
    model = FamiliaProduto
    template_name = 'familias_produto_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

class FamiliaProdutoCreateView(LicenseMixin, CreateView):
    model = FamiliaProduto
    form_class = FamiliaForm
    template_name = 'familia_produto_create.html'
    success_url = reverse_lazy('familias_produto_list')

class FamiliaProdutoUpdateView(LicenseMixin, UpdateView):
    model = FamiliaProduto
    form_class = FamiliaForm
    template_name = 'familia_produto_update.html'
    success_url = reverse_lazy('familias_produto_list')

class FamiliaProdutoDeleteView(LicenseMixin, DeleteView):
    model = FamiliaProduto
    template_name = 'familia_produto_delete.html'
    success_url = reverse_lazy('familias_produto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familia_produto'] = self.object
        return context


def saldo(request):
    licenca = getattr(request.user, 'licenca', None)
    db_name = licenca.lice_nome if licenca else 'default'  # Define o banco correto

    # Carregar produtos
    produtos = Produtos.objects.using(db_name).only('prod_nome', 'prod_codi')

    produto_selecionado = request.GET.get('produto', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Consultas para entradas e saídas com agregações diretas
    entradas = EntradaEstoque.objects.using(db_name).only('entr_prod', 'entr_tota', 'entr_data')
    saidas = SaidasEstoque.objects.using(db_name).only('said_prod', 'said_tota', 'said_data')

    # Se produto for selecionado, filtrar as entradas e saídas
    if produto_selecionado:
        entradas = entradas.filter(entr_prod__prod_codi=produto_selecionado)
        saidas = saidas.filter(said_prod__prod_codi=produto_selecionado)

    # Filtro por intervalo de data
    if data_inicio and data_fim:
        entradas = entradas.filter(entr_data__range=[data_inicio, data_fim])
        saidas = saidas.filter(said_data__range=[data_inicio, data_fim])

    # Agregação de entradas e saídas
    total_entradas = entradas.aggregate(total_entradas=Sum('entr_tota'))['total_entradas'] or 0
    total_saidas = saidas.aggregate(total_saidas=Sum('said_tota'))['total_saidas'] or 0

    # Calcular saldo
    saldo_produto_selecionado = total_entradas - total_saidas

    # Paginando as entradas e saídas
    entradas_data = list(entradas.values('entr_prod').annotate(total_entradas=Sum('entr_tota')).iterator())
    saidas_data = list(saidas.values('said_prod').annotate(total_saidas=Sum('said_tota')).iterator())

    entradas_paginator = Paginator(entradas_data, 50)
    saidas_paginator = Paginator(saidas_data, 50)

    page_entradas = request.GET.get('page_entradas', 1)
    page_saidas = request.GET.get('page_saidas', 1)
    entradas_page = entradas_paginator.get_page(page_entradas)
    saidas_page = saidas_paginator.get_page(page_saidas)

    # Passando todos os dados para o template
    return render(request, 'saldos.html', {
        'produtos': produtos,
        'produto_selecionado': produto_selecionado,
        'saldo_produto_selecionado': saldo_produto_selecionado,  # Passando o saldo
        'entradas_page': entradas_page,
        'saidas_page': saidas_page,
        'entradas_data': entradas_data[:10],  # Apenas 10 para o gráfico
        'saidas_data': saidas_data[:10]
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



def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")



def buscar_produtos(request):
    query = request.GET.get('q', '')
    produtos = Produtos.objects.filter(prod_nome__icontains=query)
    resultado = [{'prod_codi': produto.prod_codi, 'prod_nome': produto.prod_nome} for produto in produtos]
    return JsonResponse(resultado, safe=False)