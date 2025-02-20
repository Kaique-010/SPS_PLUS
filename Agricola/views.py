from django.http import HttpResponse
import csv
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CategoriaProduto, Fazenda, Talhao, ProdutoAgro, EstoqueFazenda, MovimentacaoEstoque, AplicacaoInsumos, Animal, EventoAnimal, CicloFlorestal
from .forms import CategoriaProdutoForm, FazendaForm, TalhaoForm, ProdutoAgroForm, EstoqueFazendaForm, MovimentacaoEstoqueForm, AplicacaoInsumosForm, AnimalForm, EventoAnimalForm, CicloFlorestalForm
from licencas.mixins import LicenseMixin

# Fazenda Views
class FazendaListView(LicenseMixin, ListView):
    model = Fazenda
    template_name = "fazenda_list.html"

class FazendaCreateView(LicenseMixin, CreateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agricola/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")

class FazendaUpdateView(LicenseMixin, UpdateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agricola/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")

class FazendaDeleteView(LicenseMixin, DeleteView):
    model = Fazenda
    template_name = "agricola/fazenda_confirm_delete.html"
    success_url = reverse_lazy("fazenda_list")

# Talhão Views
class TalhaoListView(LicenseMixin, ListView):
    model = Talhao
    template_name = "agricola/talhao_list.html"

class TalhaoCreateView(LicenseMixin, CreateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agricola/talhao_form.html"
    success_url = reverse_lazy("talhao_list")

class TalhaoUpdateView(LicenseMixin, UpdateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agricola/talhao_form.html"
    success_url = reverse_lazy("talhao_list")



class TalhaoDeleteView(LicenseMixin, DeleteView):
    model = Talhao
    template_name = "agricola/talhao_confirm_delete.html"
    success_url = reverse_lazy("talhao_list")




class ProdutoAgroListView(LicenseMixin, ListView):
    model = ProdutoAgro
    template_name = "agricola/produtoagro_list.html"



class ProdutoAgroCreateView(LicenseMixin, CreateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agricola/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")



class ProdutoAgroUpdateView(LicenseMixin, UpdateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agricola/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")



class ProdutoAgroDeleteView(LicenseMixin, DeleteView):
    model = ProdutoAgro
    template_name = "agricola/produtoagro_confirm_delete.html"
    success_url = reverse_lazy("produtoagro_list")




class EstoqueFazendaListView(LicenseMixin, ListView):
    model = EstoqueFazenda
    template_name = "agricola/estoquefazenda_list.html"



class EstoqueFazendaCreateView(LicenseMixin, CreateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agricola/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")



class EstoqueFazendaUpdateView(LicenseMixin, UpdateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agricola/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")



class EstoqueFazendaDeleteView(LicenseMixin, DeleteView):
    model = EstoqueFazenda
    template_name = "agricola/estoquefazenda_confirm_delete.html"
    success_url = reverse_lazy("estoquefazenda_list")



class MovimentacaoEstoqueListView(LicenseMixin, ListView):
    model = MovimentacaoEstoque
    template_name = "agricola/movimentacaoestoque_list.html"



class MovimentacaoEstoqueCreateView(LicenseMixin, CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agricola/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")



class MovimentacaoEstoqueUpdateView(LicenseMixin, UpdateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agricola/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")



class MovimentacaoEstoqueDeleteView(LicenseMixin, DeleteView):
    model = MovimentacaoEstoque
    template_name = "agricola/movimentacaoestoque_confirm_delete.html"
    success_url = reverse_lazy("movimentacaoestoque_list")




class AplicacaoInsumosListView(LicenseMixin, ListView):
    model = AplicacaoInsumos
    template_name = "agricola/aplicacaoinsumos_list.html"



class AplicacaoInsumosCreateView(LicenseMixin, CreateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agricola/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")



class AplicacaoInsumosUpdateView(LicenseMixin, UpdateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agricola/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")



class AplicacaoInsumosDeleteView(LicenseMixin, DeleteView):
    model = AplicacaoInsumos
    template_name = "agricola/aplicacaoinsumos_confirm_delete.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")




class AnimalListView(LicenseMixin, ListView):
    model = Animal
    template_name = "agricola/animal_list.html"




class AnimalCreateView(LicenseMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agricola/animal_form.html"
    success_url = reverse_lazy("animal_list")




class AnimalUpdateView(LicenseMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agricola/animal_form.html"
    success_url = reverse_lazy("animal_list")



class AnimalDeleteView(LicenseMixin, DeleteView):
    model = Animal
    template_name = "agricola/animal_confirm_delete.html"
    success_url = reverse_lazy("animal_list")
    


class EventoAnimalListView(LicenseMixin, ListView):
    model = EventoAnimal
    template_name = "agricola/eventoanimal_list.html"



class EventoAnimalCreateView(LicenseMixin, CreateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agricola/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")



class EventoAnimalUpdateView(LicenseMixin, UpdateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agricola/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")



class EventoAnimalDeleteView(LicenseMixin, DeleteView):
    model = EventoAnimal
    template_name = "agricola/eventoanimal_confirm_delete.html"
    success_url = reverse_lazy("eventoanimal_list")
    



class CicloFlorestalListView(LicenseMixin, ListView):
    model = CicloFlorestal
    template_name = "agricola/cicloflorestal_list.html"



class CicloFlorestalCreateView(LicenseMixin, CreateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agricola/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")



class CicloFlorestalUpdateView(LicenseMixin, UpdateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agricola/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")



class CicloFlorestalDeleteView(LicenseMixin, DeleteView):
    model = CicloFlorestal
    template_name = "agricola/cicloflorestal_confirm_delete.html"
    success_url = reverse_lazy("cicloflorestal_list")



# Categoria Produto Views
class CategoriaProdutoListView(LicenseMixin, ListView):
    model = CategoriaProduto
    template_name = "agricola/categoria_produto_list.html"



class CategoriaProdutoCreateView(LicenseMixin, CreateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agricola/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")



class CategoriaProdutoUpdateView(LicenseMixin, UpdateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agricola/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")



class CategoriaProdutoDeleteView(LicenseMixin, DeleteView):
    model = CategoriaProduto
    template_name = "agricola/categoria_produto_confirm_delete.html"
    success_url = reverse_lazy("categoria_produto_list")


class RelatorioMovimentacoesView(ListView):
    model = MovimentacaoEstoque
    template_name = "agricola/relatorio_movimentacoes.html"
    context_object_name = "movimentacoes"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
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
        writer.writerow(['Data', 'Tipo', 'Produto', 'Quantidade', 'Observações'])  # Cabeçalho

        for movimentacao in movimentacoes:
            writer.writerow([movimentacao.data, movimentacao.tipo, movimentacao.produto, movimentacao.quantidade, movimentacao.observacoes])
        
        return response