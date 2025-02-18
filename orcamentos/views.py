from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.db.models import Q
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
    paginate_by = 20

    def get_queryset(self):
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'

        # Ordenar explicitamente o QuerySet aqui
        orcamentos = Orcamento.objects.using(db_name).select_related('pedi_forn', 'pedi_vend').order_by('pedi_nume')  # Ordenação explícita

        for orc in orcamentos:
            print(f"Orçamento {orc.pedi_nume} - Cliente: {orc.pedi_forn.enti_nome if orc.pedi_forn else 'N/A'} - "
                  f"Vendedor: {orc.pedi_vend.enti_nome if orc.pedi_vend else ''}")

        return orcamentos


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

        # Buscar dados de cliente e vendedor
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'

        # Aqui você pode adicionar as entidades relacionadas ao orçamento
        context['clientes'] = Orcamento.objects.using(db_name).values('pedi_forn__enti_nome')  # Exemplo de cliente
        context['vendedores'] = Orcamento.objects.using(db_name).values('pedi_vend__enti_nome')  # Exemplo de vendedor

        return context

    def form_valid(self, form):
        orcamento = form.save(commit=False)

        # Obtém a licença do usuário e define o banco correto
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'

        # Salva o orçamento no banco correto
        orcamento.save(using=db_name)

        context = self.get_context_data()
        pecas_formset = context['pecas_formset']

        if pecas_formset.is_valid():
            pecas_formset.instance = orcamento

            for peca_form in pecas_formset:
                peca = peca_form.save(commit=False)
                peca.peca_empr = orcamento.pedi_empr
                peca.peca_fili = orcamento.pedi_fili

                # Salva a peça no banco correto
                peca.save(using=db_name)

            pecas_formset.save()

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

        # Buscar dados de cliente e vendedor
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'

        # Aqui você pode adicionar as entidades relacionadas ao orçamento
        context['clientes'] = Orcamento.objects.using(db_name).values('pedi_forn__enti_nome')  # Exemplo de cliente
        context['vendedores'] = Orcamento.objects.using(db_name).values('pedi_vend__enti_nome')  # Exemplo de vendedor

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
    query = request.GET.get('term', '').strip()
    licenca = getattr(request.user, 'licenca', None)
    db_name = licenca.lice_nome if licenca else 'default' 
    
    if query:
       
        produtos = Produtos.objects.using(db_name).filter(prod_nome__icontains=query)[:10]
    else:
        produtos = Produtos.objects.all()
    
    resultado = [{
        'id': produto.prod_codi,
        'nome': produto.prod_nome,
        'codigo': produto.prod_codi,
    } for produto in produtos]
    
    return JsonResponse(resultado, safe=False)