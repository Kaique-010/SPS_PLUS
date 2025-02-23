from django.db import IntegrityError
from django.forms import ValidationError
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
import csv
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sps_plus import settings
from .models import CategoriaProduto, Fazenda, Talhao, ProdutoAgro, EstoqueFazenda, MovimentacaoEstoque, AplicacaoInsumos, Animal, EventoAnimal, CicloFlorestal
from .forms import CategoriaProdutoForm, FazendaForm, TalhaoForm, ProdutoAgroForm, EstoqueFazendaForm, MovimentacaoEstoqueForm, AplicacaoInsumosForm, AnimalForm, EventoAnimalForm, CicloFlorestalForm



class FazendaListView( ListView):
    model = Fazenda
    template_name = "fazenda_list.html"
    context_object_name = 'fazendas'
    
    def get_queryset(self):
        # Obtém a licença do usuário a partir do mixin
        user_licenca = self.request.user.licenca
        db_name = user_licenca.lice_nome if user_licenca else "default"

        queryset = Fazenda.objects.using(db_name).order_by('empr_faze')

        

        return queryset

class FazendaCreateView( CreateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agricola/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")
    
    def get_queryset(self):
        # Obtém a licença do usuário a partir do mixin
        user_licenca = self.request.user.licenca
        db_name = user_licenca.lice_nome if user_licenca else "default"

        queryset = Fazenda.objects.using(db_name).order_by('empr_faze')

        

        return queryset
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Passa o request para o formulário
        return kwargs


class FazendaUpdateView( UpdateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agricola/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")


class FazendaDeleteView( DeleteView):
    model = Fazenda
    template_name = "agricola/fazenda_confirm_delete.html"
    success_url = reverse_lazy("fazenda_list")



# Talhão Views
class TalhaoListView( ListView):
    model = Talhao
    template_name = "agricola/talhao_list.html"
    context_object_name = 'talhoes'


class TalhaoCreateView( CreateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agricola/talhao_form.html"
    success_url = reverse_lazy("talhao_list")



class TalhaoUpdateView( UpdateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agricola/talhao_form.html"
    success_url = reverse_lazy("talhao_list")
    


class TalhaoDeleteView( DeleteView):
    model = Talhao
    template_name = "agricola/talhao_confirm_delete.html"
    success_url = reverse_lazy("talhao_list")


# Produto Agro Views
class ProdutoAgroListView( ListView):
    model = ProdutoAgro
    template_name = "agricola/produtoagro_list.html"


class ProdutoAgroCreateView( CreateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agricola/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")


class ProdutoAgroUpdateView( UpdateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agricola/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")


class ProdutoAgroDeleteView( DeleteView):
    model = ProdutoAgro
    template_name = "agricola/produtoagro_confirm_delete.html"
    success_url = reverse_lazy("produtoagro_list")


# Estoque Fazenda Views
class EstoqueFazendaListView( ListView):
    model = EstoqueFazenda
    template_name = "agricola/estoquefazenda_list.html"


class EstoqueFazendaCreateView( CreateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agricola/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")



class EstoqueFazendaUpdateView( UpdateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agricola/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")


class EstoqueFazendaDeleteView( DeleteView):
    model = EstoqueFazenda
    template_name = "agricola/estoquefazenda_confirm_delete.html"
    success_url = reverse_lazy("estoquefazenda_list")


# Movimentação Estoque Views
class MovimentacaoEstoqueListView( ListView):
    model = MovimentacaoEstoque
    template_name = "agricola/movimentacaoestoque_list.html"


class MovimentacaoEstoqueCreateView( CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agricola/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")


class MovimentacaoEstoqueUpdateView( UpdateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agricola/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")



class MovimentacaoEstoqueDeleteView( DeleteView):
    model = MovimentacaoEstoque
    template_name = "agricola/movimentacaoestoque_confirm_delete.html"
    success_url = reverse_lazy("movimentacaoestoque_list")


# Aplicacao Insumos Views
class AplicacaoInsumosListView( ListView):
    model = AplicacaoInsumos
    template_name = "agricola/aplicacaoinsumos_list.html"


class AplicacaoInsumosCreateView( CreateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agricola/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")



class AplicacaoInsumosUpdateView( UpdateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agricola/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")



class AplicacaoInsumosDeleteView( DeleteView):
    model = AplicacaoInsumos
    template_name = "agricola/aplicacaoinsumos_confirm_delete.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")


# Animal Views
class AnimalListView( ListView):
    model = Animal
    template_name = "agricola/animal_list.html"


class AnimalCreateView( CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agricola/animal_form.html"
    success_url = reverse_lazy("animal_list")



class AnimalUpdateView( UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agricola/animal_form.html"
    success_url = reverse_lazy("animal_list")



class AnimalDeleteView( DeleteView):
    model = Animal
    template_name = "agricola/animal_confirm_delete.html"
    success_url = reverse_lazy("animal_list")

# Evento Animal Views
class EventoAnimalListView( ListView):
    model = EventoAnimal
    template_name = "agricola/eventoanimal_list.html"


class EventoAnimalCreateView( CreateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agricola/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")


class EventoAnimalUpdateView( UpdateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agricola/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")


class EventoAnimalDeleteView( DeleteView):
    model = EventoAnimal
    template_name = "agricola/eventoanimal_confirm_delete.html"
    success_url = reverse_lazy("eventoanimal_list")


# Ciclo Florestal Views
class CicloFlorestalListView( ListView):
    model = CicloFlorestal
    template_name = "agricola/cicloflorestal_list.html"


class CicloFlorestalCreateView( CreateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agricola/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")


class CicloFlorestalUpdateView( UpdateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agricola/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")


class CicloFlorestalDeleteView( DeleteView):
    model = CicloFlorestal
    template_name = "agricola/cicloflorestal_confirm_delete.html"
    success_url = reverse_lazy("cicloflorestal_list")

# Categoria Produto Views
class CategoriaProdutoListView( ListView):
    model = CategoriaProduto
    template_name = "agricola/categoria_produto_list.html"



class CategoriaProdutoCreateView( CreateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agricola/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")


class CategoriaProdutoUpdateView( UpdateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agricola/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")

class CategoriaProdutoDeleteView( DeleteView):
    model = CategoriaProduto
    template_name = "agricola/categoria_produto_confirm_delete.html"
    success_url = reverse_lazy("categoria_produto_list")





# Relatório Movimentações
class RelatorioMovimentacoesView( ListView):
    model = MovimentacaoEstoque
    template_name = "agricola/relatorio_movimentacoes.html"
    context_object_name = "movimentacoes"
    
    def get_queryset(self):
        queryset = MovimentacaoEstoque.objects.using(self.db_name).filter(estoque__fazenda__licenca=self.get_license())
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        tipo = self.request.GET.get('tipo')

        if data_inicial and data_final:
            queryset = queryset.filter(data__range=[data_inicial, data_final])
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset

    def get(self, request, *args, **kwargs):
        if request.GET.get('exportar') == 'true':
            return self.exportar_movimentacoes()
        return super().get(request, *args, **kwargs)

    def exportar_movimentacoes(self):
        movimentacoes = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="movimentacoes.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Data', 'Tipo', 'Produto', 'Quantidade', 'Observações'])

        for movimentacao in movimentacoes:
            writer.writerow([movimentacao.data, movimentacao.tipo, movimentacao.produto, movimentacao.quantidade, movimentacao.observacoes])
        
        return response
