from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from produto.models import Produtos
from .models import Orcamento, OrcamentoPecas
from .forms import OrcamentoForm, OrcamentoPecasForm, OrcamentoPecasInlineFormSet

class OrcamentoListView(ListView):
    model = Orcamento
    template_name = "orcamentos/orcamento_list.html"
    context_object_name = "orcamentos"
    ordering = ['-orca_id']  

class OrcamentoCreateView(CreateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = "orcamentos/orcamento_form.html"
    success_url = reverse_lazy("orcamento_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['pecas_formset'] = OrcamentoPecasInlineFormSet(self.request.POST)
        else:
            context['pecas_formset'] = OrcamentoPecasInlineFormSet()
        return context

    def form_valid(self, form):
        # Cria o orçamento, mas não salva imediatamente
        orcamento = form.save(commit=False)
        
        # Salva o orçamento para garantir que ele tenha um ID
        orcamento.save()

        # Obtém o formset de peças
        context = self.get_context_data()
        pecas_formset = context['pecas_formset']

        # Se o formset de peças for válido
        if pecas_formset.is_valid():
            # Associa o orçamento com as peças
            pecas_formset.instance = orcamento  # Associa o orçamento com as peças

            # Preenche os campos orca_empr e orca_fili nas peças antes de salvar
            for peca_form in pecas_formset:
                peca = peca_form.save(commit=False)
                peca.peca_empr = orcamento.orca_empr  
                peca.peca_fili = orcamento.orca_fili 
            
                

            # Agora salva o formset de peças de uma vez
            pecas_formset.save()  # Salva todas as peças de uma vez

        # Redireciona após salvar orçamento e peças
        return redirect(self.success_url)


class OrcamentoUpdateView(UpdateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'orcamentos/orcamento_form.html'
    success_url = reverse_lazy('orcamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['pecas_formset'] = OrcamentoPecasInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['pecas_formset'] = OrcamentoPecasInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        orcamento = form.save(commit=False)
        context = self.get_context_data()
        pecas_formset = context['pecas_formset']

        # Salva o orçamento primeiro (mas ainda sem commit)
        orcamento.save()  # Agora o orçamento está salvo e pode ser usado para preencher as peças

        if pecas_formset.is_valid():
            pecas_formset.instance = orcamento  # Associa as peças ao orçamento

            # Preenche os campos orca_empr e orca_fili nas peças antes de salvar
            for peca_form in pecas_formset:
                peca = peca_form.save(commit=False)
                peca.peca_empr = orcamento.orca_empr
                peca.peca_fili = orcamento.orca_fili
                peca.save()  # Salva a peça com os valores preenchidos corretamente

        return redirect(self.success_url)  # Redireciona após salvar orçamento e peças


class OrcamentoDetailView(DetailView):
    model = Orcamento
    template_name = "orcamentos/orcamento_detail.html"
    context_object_name = "orcamento"


class OrcamentoDeleteView(DeleteView):
    model = Orcamento
    template_name = 'orcamentos/orcamento_confirm_delete.html'
    success_url = reverse_lazy('orcamento_list')
    
    


def buscar_produtos(request):
    query = request.GET.get('q', '')
    produtos = Produtos.objects.filter(nome__icontains=query)
    resultado = [{'id': produtos.prod_codi, 'nome': produtos.prod_desc} for produto in produtos]
    return JsonResponse(resultado, safe=False)