from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from licencas.utils import current_alias
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from Entidades.models import Entidades
from produto.models import Produtos
from .models import Orcamentos, ItensOrcamento
from .forms import OrcamentoForm, OrcamentoPecasForm, OrcamentoPecasInlineFormSet

class OrcamentoListView(ListView):
    model = Orcamentos  
    template_name = "orcamentos/orcamento_list.html"
    context_object_name = "orcamentos"
    paginate_by = 10

    def get_queryset(self):
        alias = current_alias(self.request)

        numero = self.request.GET.get('pedi_nume', '').strip()
        cliente = self.request.GET.get('pedi_forn', '').strip()
        vendedor = self.request.GET.get('pedi_vend', '').strip()

        orcamentos = Orcamentos.objects.using(alias).order_by('pedi_nume')

        if numero:
            orcamentos = orcamentos.filter(pedi_nume__icontains=numero)

        if cliente:
            orcamentos = orcamentos.filter(pedi_forn__icontains=cliente)

        if vendedor:
            orcamentos = orcamentos.filter(pedi_vend__icontains=vendedor)

        return orcamentos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedi_nume'] = self.request.GET.get('pedi_nume', '')
        context['pedi_forn'] = self.request.GET.get('pedi_forn', '')
        context['pedi_vend'] = self.request.GET.get('pedi_vend', '')
        return context


class OrcamentoCreateView(CreateView):
    model = Orcamentos
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
        alias = current_alias(self.request)

        context['clientes'] = Entidades.objects.using(alias).filter(enti_tipo_enti='CL')
        context['vendedores'] = Entidades.objects.using(alias).filter(enti_tipo_enti__in=['VE', 'AM'])

        return context

    def form_valid(self, form):
        print("🔹 Dados do POST:", self.request.POST)

        orcamento = form.save(commit=False)
        alias = current_alias(self.request)
        orcamento.save(using=alias)

        pecas_formset = OrcamentoPecasInlineFormSet(self.request.POST, instance=orcamento)

        if pecas_formset.is_valid():
            pecas = pecas_formset.save(commit=False)

            for peca in pecas:
                # Preencher campos auxiliares antes de salvar
                peca.iped_empr = orcamento.pedi_empr
                peca.iped_fili = orcamento.pedi_fili
                peca.save(using=alias)

            messages.success(self.request, "Orçamento salvo com sucesso!")

            return super().form_valid(form)

        else:
            print("❌ Erros no formset:", pecas_formset.errors)

        # Se o formset não for válido, adicionar erros ao form principal e chamar form_invalid
        for erro in pecas_formset.errors:
            form.add_error(None, erro)

        return self.form_invalid(form)


class OrcamentoUpdateView(UpdateView):
    model = Orcamentos
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
        alias = current_alias(self.request)

        context['clientes'] = Entidades.objects.using(alias).filter(enti_tipo_enti='CL')
        context['vendedores'] = Entidades.objects.using(alias).filter(enti_tipo_enti__in=['VE', 'AM'])

        return context

    def form_valid(self, form):
        orcamento = form.save(commit=False)
        alias = current_alias(self.request)
        orcamento.save(using=alias)

        pecas_formset = OrcamentoPecasInlineFormSet(self.request.POST, instance=orcamento)

        if pecas_formset.is_valid():
            pecas = pecas_formset.save(commit=False)
            for peca in pecas:
                peca.iped_empr = orcamento.pedi_empr
                peca.iped_fili = orcamento.pedi_fili
                peca.save(using=alias)

        return redirect(self.success_url)



class OrcamentoDetailView(DetailView):
    model = Orcamentos  
    template_name = "orcamentos/orcamento_detail.html"
    context_object_name = "orcamento"


class OrcamentoDeleteView(DeleteView):
    model = Orcamentos   
    template_name = 'orcamentos/orcamento_confirm_delete.html'
    success_url = reverse_lazy('orcamento_list')    
    
    
    
def buscar_produtos(request):
    query = request.GET.get('term', '').strip()
    alias = current_alias(request)

    if query:
        produtos = Produtos.objects.using(alias).filter(prod_nome__icontains=query)[:10]
    else:
        produtos = Produtos.objects.using(alias).all()
    
    resultado = [{
        'id': produto.prod_codi,
        'nome': produto.prod_nome,
        'codigo': produto.prod_codi,
    } for produto in produtos]
    
    return JsonResponse(resultado, safe=False)


def buscar_clientes(request):
    term = request.GET.get('term', '').strip()
    alias = current_alias(request)

    if term:
        clientes = Entidades.objects.using(alias).filter(
            enti_tipo_enti__in=['CL', 'AM'], 
            enti_nome__icontains=term
        )[:10]
    else:
        clientes = Entidades.objects.using(alias).filter(
            enti_tipo_enti__in=['CL', 'AM']
        )[:10]
    
    data = [{'id': cliente.enti_clie, 'nome': cliente.enti_nome} for cliente in clientes]
    return JsonResponse(data, safe=False)

def buscar_vendedores(request):
    term = request.GET.get('term', '').strip()
    alias = current_alias(request)

    if term:
        vendedores = Entidades.objects.using(alias).filter(
            enti_tipo_enti__in=['VE', 'AM'], 
            enti_nome__icontains=term
        )[:10]
    else:
        vendedores = Entidades.objects.using(alias).filter(
            enti_tipo_enti__in=['VE', 'AM']
        )[:10]

    data = [{'id': vendedor.enti_clie, 'nome': vendedor.enti_nome} for vendedor in vendedores]
    return JsonResponse(data, safe=False)
