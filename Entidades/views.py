from io import BytesIO
from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.db import connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import openpyxl
import requests
from .models import Entidades
from django.db.models import Max
from .serializers import EntidadesSerializer
from .forms import EntidadesForm 
from rest_framework import viewsets
from rest_framework import filters
from django.core.paginator import Paginator
from Entidades import models
from licencas.utils import current_alias


    

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
@method_decorator(login_required, name='dispatch')    
class EntidadesListView( ListView):
    model = Entidades
    template_name = 'entidades.html'
    context_object_name = 'entidades'
    paginate_by = 15

    def get_queryset(self):
        alias = current_alias(self.request)
        queryset = Entidades.objects.using(alias).order_by('enti_clie')

        nome = self.request.GET.get('enti_nome')
        enti_clie = self.request.GET.get('enti_clie')

        if nome:
            queryset = queryset.filter(enti_nome__icontains=nome)

        if enti_clie:
            queryset = queryset.filter(enti_clie=enti_clie)

        return queryset

class EntidadeCreateView(CreateView):
    model = Entidades
    form_class = EntidadesForm
    template_name = 'entidade_form.html'
    success_url = reverse_lazy('entidades')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Passa o request para o formulário
        return kwargs

class EntidadeUpdateView(UpdateView):
    model = Entidades
    form_class = EntidadesForm
    template_name = 'entidade_form.html'  # Template de edição
    success_url = reverse_lazy('entidades')  # URL para redirecionar após a atualização

    def get_object(self, queryset=None):
        # Obtém o objeto do banco de dados do cliente atual
        db_alias = current_alias(self.request)

        # Captura o pk da URL
        enti_clie = self.kwargs.get('enti_clie')
        if not enti_clie:
            raise ValueError("Erro: Enti_clie não encontrado na URL.")

        # Busca o objeto no banco de dados ativo
        obj = get_object_or_404(Entidades.objects.using(db_alias), enti_clie=enti_clie)
        return obj

    def get_form_kwargs(self):
        # Passa o request para o formulário
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class EntidadeDeleteView(DeleteView):
    model = Entidades
    template_name = 'entidade_confirm_delete.html'  # Template de confirmação de exclusão
    success_url = reverse_lazy('entidades')  # URL para redirecionar após a exclusão

    def get_object(self, queryset=None):
        # Obtém o objeto do banco de dados do cliente atual
        db_alias = current_alias(self.request)

        # Captura o pk da URL
        pk = self.kwargs.get('enti_clie')
        if not pk:
            raise ValueError("Erro: pk não encontrado na URL.")

        # Busca o objeto no banco de dados ativo
        obj = get_object_or_404(Entidades.objects.using(db_alias), pk=pk)
        return obj








def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None



def exportar_entidades(request):
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Pessoas'

    # Define o cabeçalho
    columns = ['ID', 'Nome', 'CPF', 'CIDADE',  'ESTADO', 'CNPJ', 'IE', 'E-MAIL','CELULAR', 'TELEFONE', 'Classificação']
    worksheet.append(columns)

    entidades = Entidades.objects.all()
    
    for entidade in entidades:
        worksheet.append([
            entidade.enti_nume,
            entidade.enti_nome,
            entidade.enti_cpf,
            entidade.enti_cida,
            entidade.enti_esta,
            entidade.enti_cnpj,
            entidade.enti_insc_esta,
            entidade.enti_emai,
            entidade.enti_celu,
            entidade.enti_fone,
            entidade.enti_tipo_enti
        ])
    
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=entidades.xlsx'
    return response