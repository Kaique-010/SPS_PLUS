from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class EntradasListView(ListView):
    model = models.Entrada_Produtos
    template_name = 'entradaslistas.html'
    context_object_name = 'entradas'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')

        if produto:
            # Filtrando pelo nome do produto relacionado
            queryset = queryset.filter(produto__nome_produto__icontains=produto)

        return queryset
    

class EntradasCreateView(CreateView):
    model = models.Entrada_Produtos
    template_name = 'entradascriar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

class EntradasDetailView(DetailView):
    model = models.Entrada_Produtos
    template_name = 'entradasdetalhe.html'


class EntradasUpdateView(UpdateView):
    model = models.Entrada_Produtos
    template_name = 'entradaseditar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')



class EntradasDeleteView(DeleteView):
    model = models.Entrada_Produtos
    template_name = 'entradasexcluir.html'
    success_url = reverse_lazy('entradaslistas')




    
