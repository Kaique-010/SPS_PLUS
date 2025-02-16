from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy
from Entidades.models  import Entidades
from produto.models import Produtos
from licencas.mixins import LicenseMixin

class EntradasListView(ListView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradaslistas.html'
    context_object_name = 'entradas'
    paginate_by = 5

    def get_queryset(self):
        licenca = self.get_license()  # Obtém a licença associada ao usuário
        db_name = licenca.lice_nome if licenca else 'default'

        queryset = models.EntradaEstoque.objects.using(db_name)  # Utiliza o banco correto para a consulta
        produto = self.request.GET.get('produto')

        if produto:
            queryset = queryset.filter(entr_prod__prod_nome__icontains=produto)

        return queryset

    

class EntradasCreateView(CreateView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradascriar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

    def form_valid(self, form):
        # Obter o nome do banco de dados da licença
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else 'default'
        
        # Definir o banco de dados para a instância
        form.instance._state.db = db_name

        return super().form_valid(form)

class EntradasDeleteView(DeleteView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradasexcluir.html'
    success_url = reverse_lazy('entradaslistas')

    def get_object(self, queryset=None):
        # Obter o nome do banco de dados da licença
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else 'default'

        # Garantir que a consulta use o banco correto
        return super().get_object(queryset).using(db_name)



class EntradasUpdateView(UpdateView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradaseditar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

class EntradasDetailView(DetailView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradasdetalhe.html'

    def get_object(self, queryset=None):
        # Obter o nome do banco de dados da licença
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else 'default'

        # Garantir que a consulta use o banco correto
        return super().get_object(queryset).using(db_name)


class EntradasDeleteView(DeleteView, LicenseMixin):
    model = models.EntradaEstoque
    template_name = 'entradasexcluir.html'
    success_url = reverse_lazy('entradaslistas')




    
