from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class SaidasListView(ListView):
    model = models.Saida_Produtos
    template_name = 'saidaslistas.html'
    context_object_name = 'saidas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')

        if produto:
            # Filtrando pelo nome do produto relacionado
            queryset = queryset.filter(produto__nome_produto__icontains=produto)

        return queryset


class SaidasCreateView(CreateView):
    model = models.Saida_Produtos
    template_name = 'saidascriar.html'
    form_class = forms.Saidas
    success_url = reverse_lazy('saidaslistas')


class SaidasDetailView(DetailView):
    model = models.Saida_Produtos
    template_name = 'saidasdetalhe.html'


class SaidasUpdateView(UpdateView):
    model = models.Saida_Produtos
    template_name = 'saidaseditar.html'
    form_class = forms.Saidas
    success_url = reverse_lazy('saidaslistas')



class SaidasDeleteView(DeleteView):
    model = models.Saida_Produtos
    template_name = 'saidasexcluir.html'
    success_url = reverse_lazy('saidaslistas')




    
