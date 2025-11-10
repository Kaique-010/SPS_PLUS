from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy
from Entidades.models  import Entidades
from produto.models import Produtos
from licencas.utils import current_alias

class EntradasListView(ListView):
    model = models.EntradaEstoque
    template_name = 'entradaslistas.html'
    context_object_name = 'entradas'
    paginate_by = 5

    def get_queryset(self):
        alias = current_alias(self.request)

        queryset = models.EntradaEstoque.objects.using(alias)  # Utiliza o banco correto para a consulta
        produto = self.request.GET.get('produto')

        if produto:
            queryset = queryset.filter(entr_prod__prod_nome__icontains=produto)

        return queryset

    

class EntradasCreateView(CreateView):
    model = models.EntradaEstoque
    template_name = 'entradascriar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

    def form_valid(self, form):
        alias = current_alias(self.request)
        # Definir o banco de dados para a instância
        form.instance._state.db = alias

        return super().form_valid(form)

class EntradasDeleteView(DeleteView):
    model = models.EntradaEstoque
    template_name = 'entradasexcluir.html'
    success_url = reverse_lazy('entradaslistas')

    def get_object(self, queryset=None):
        alias = current_alias(self.request)
        # Garantir que a consulta use o banco correto
        return super().get_object(queryset).using(alias)



class EntradasUpdateView(UpdateView):
    model = models.EntradaEstoque
    template_name = 'entradaseditar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

class EntradasDetailView(DetailView):
    model = models.EntradaEstoque
    template_name = 'entradasdetalhe.html'

    def get_object(self, queryset=None):
        alias = current_alias(self.request)
        # Garantir que a consulta use o banco correto
        return super().get_object(queryset).using(alias)


# Removido bloco duplicado de EntradasDeleteView com lógica antiga baseada em request.user.licenca



    
