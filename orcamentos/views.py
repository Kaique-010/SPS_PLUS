from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from Entidades.models import Entidades
from produto.models import Produtos
from .models import Orcamento, OrcamentoPecas
from .forms import OrcamentoForm, OrcamentoPecasForm, OrcamentoPecasInlineFormSet

class OrcamentoListView(ListView):
    model = Orcamento
    template_name = "orcamentos/orcamento_list.html"
    context_object_name = "orcamentos"
    paginate_by = 10

    def get_queryset(self):
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'

        numero = self.request.GET.get('pedi_nume', '').strip()
        cliente = self.request.GET.get('pedi_forn', '').strip()
        vendedor = self.request.GET.get('pedi_vend', '').strip()

        orcamentos = Orcamento.objects.using(db_name).select_related('pedi_forn', 'pedi_vend').order_by('pedi_nume')

        if numero:
            orcamentos = orcamentos.filter(pedi_nume__icontains=numero)

        if cliente:
            orcamentos = orcamentos.filter(pedi_forn__enti_nome__icontains=cliente)

        if vendedor:
            orcamentos = orcamentos.filter(pedi_vend__enti_nome__icontains=vendedor)

        return orcamentos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedi_nume'] = self.request.GET.get('pedi_nume', '')
        context['pedi_forn'] = self.request.GET.get('pedi_forn', '')
        context['pedi_vend'] = self.request.GET.get('pedi_vend', '')
        return context


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

        context['clientes'] = Entidades.objects.using(db_name).filter(enti_tipo_enti='CL')
        context['vendedores'] = Entidades.objects.using(db_name).filter(enti_tipo_enti__in=['VE', 'AM'])

        return context

    def form_valid(self, form):
        print("🔹 Dados do POST:", self.request.POST)  # Debug

        orcamento = form.save(commit=False)
        licenca = getattr(self.request.user, 'licenca', None)
        db_name = licenca.lice_nome if licenca else 'default'
        orcamento.save(using=db_name)  # Salvar corretamente no banco correto

        pecas_formset = OrcamentoPecasInlineFormSet(self.request.POST, instance=orcamento)

        if pecas_formset.is_valid():
            pecas = pecas_formset.save(commit=False)

            for peca in pecas:
                produto = Produtos.objects.using(db_name).filter(prod_codi=peca.peca_codi).first()
                if produto:
                    peca.peca_codi = produto  # Associa o objeto correto
                    peca.peca_empr = orcamento.pedi_empr
                    peca.peca_fili = orcamento.pedi_fili
                    peca.save(using=db_name)

            messages.success(self.request, "Orçamento salvo com sucesso!")

            return super().form_valid(form)  # Chamar a função corretamente

        else:
            form.add_error(None, f"Produto com código {peca.peca_codi} não encontrado!")
            print("❌ Erros no formset:", pecas_formset.errors)  # Debug para ver erros do formset

        # Se o formset não for válido, adicionar erros ao form principal e chamar form_invalid
        for erro in pecas_formset.errors:
            form.add_error(None, erro)

        return self.form_invalid(form)


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


def buscar_clientes(request):
    term = request.GET.get('term', '').strip()
    licenca = getattr(request.user, 'licenca', None)
    db_name = licenca.lice_nome if licenca else 'default'

    if term:
        clientes = Entidades.objects.using(db_name).filter(
            enti_tipo_enti__in=['CL', 'AM'], 
            enti_nome__icontains=term
        )[:10]
    else:
        clientes = Entidades.objects.using(db_name).filter(
            enti_tipo_enti__in=['CL', 'AM']
        )[:10]
    
    data = [{'id': cliente.enti_clie, 'nome': cliente.enti_nome} for cliente in clientes]
    return JsonResponse(data, safe=False)

def buscar_vendedores(request):
    term = request.GET.get('term', '').strip()
    licenca = getattr(request.user, 'licenca', None)
    db_name = licenca.lice_nome if licenca else 'default'

    if term:
        vendedores = Entidades.objects.using(db_name).filter(
            enti_tipo_enti__in=['VE', 'AM'], 
            enti_nome__icontains=term
        )[:10]
    else:
        vendedores = Entidades.objects.using(db_name).filter(
            enti_tipo_enti__in=['VE', 'AM']
        )[:10]

    data = [{'id': vendedor.enti_clie, 'nome': vendedor.enti_nome} for vendedor in vendedores]
    return JsonResponse(data, safe=False)
