from io import BytesIO
from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.db import connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
import openpyxl
import requests
from licencas.mixins import LicenseMixin
from .models import Entidades
from django.db.models import Max
from .serializers import EntidadesSerializer
from .forms import EntidadesForm 
from rest_framework import viewsets
from rest_framework import filters
from django.core.paginator import Paginator
from Entidades import models


    

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
    
class EntidadesListView(LicenseMixin, ListView):
    model = Entidades
    template_name = 'entidades.html'
    context_object_name = 'entidades'
    paginate_by = 15

    def get_queryset(self):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"

        queryset = Entidades.objects.using(db_name).order_by('enti_clie')

        nome = self.request.GET.get('enti_nome')
        enti_clie = self.request.GET.get('enti_clie')

        if nome:
            queryset = queryset.filter(enti_nome__icontains=nome)

        if enti_clie:
            queryset = queryset.filter(enti_clie=enti_clie)

        return queryset




class EntidadeCreateView(LicenseMixin, CreateView):
    model = models.Entidades
    form_class = EntidadesForm
    template_name = 'entidade_form.html'
    success_url = reverse_lazy('entidades')

    def dispatch(self, request, *args, **kwargs):
        """ Garante que o banco da licença está definido na sessão antes de processar a requisição """
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else None

        if not db_name:
            print("🚨 Erro: Nenhuma licença encontrada ou nome do banco indefinido!")
            return redirect('erro_view')  # Redireciona para uma página de erro apropriada

        # Define o banco na sessão
        request.session['banco'] = db_name
        request.session.modified = True

        print(f"✅ Banco de dados definido na sessão: {request.session.get('banco')}")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['db_name'] = self.request.session.get('banco')  # Passa o nome do banco da sessão
        return kwargs
    
    def form_valid(self, form):
        """ Valida o formulário e salva a entidade no banco correto """
        db_name = self.request.session.get('banco')

        print(f"📌 Banco de dados na sessão antes de salvar: {db_name}")

        if not db_name:
            form.add_error(None, "Erro: banco de dados não definido.")
            return self.form_invalid(form)

        # Passa o banco de dados para o formulário
        form.instance._state.db = db_name

        print(f"📌 Tentando salvar no banco: {db_name}")

        try:
            response = super().form_valid(form)  # Aqui o Django já chama `save()`
            messages.success(self.request, "Entidade criada com sucesso!")
            return response
        except Exception as e:
            form.add_error(None, f"Erro ao salvar a entidade: {e}")
            return self.form_invalid(form)

    def get_success_url(self):
        # Confirma que a licença ainda está disponível antes de redirecionar
        if not self.get_license():
            print("🚨 Erro: Licença não encontrada antes de redirecionar!")
            return redirect('erro_view')  # Redireciona para uma página de erro apropriada
        return super().get_success_url()




class EntidadeUpdateView(LicenseMixin, UpdateView):
    model = models.Entidades
    form_class = EntidadesForm
    template_name = 'entidade_form.html'
    success_url = reverse_lazy('entidades')

    def get_object(self, queryset=None):
        licenca = self.get_license()
        db_name = licenca.lice_nome if licenca else "default"
        enti_clie = self.kwargs.get("enti_clie")

        print(f"[DEBUG] Buscando entidade com enti_clie={enti_clie} no banco {db_name}")

        entidade = models.Entidades.objects.using(db_name).filter(enti_clie=enti_clie).first()
        
        if not entidade:
            raise Http404("Entidade não encontrada.")
        
        return entidade

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['db_name'] = self.request.session.get('banco')  # Passa o nome do banco da sessão
        return kwargs
    
    def form_valid(self, form):
        """ Valida o formulário e salva a entidade no banco correto """
        db_name = self.request.session.get('banco')

        print(f"📌 Banco de dados na sessão antes de salvar: {db_name}")

        if not db_name:
            form.add_error(None, "Erro: banco de dados não definido.")
            return self.form_invalid(form)

        # Obtém o objeto correto para edição
        entidade = self.get_object()

        # Atualiza os campos da entidade com os dados do formulário
        for field, value in form.cleaned_data.items():
            setattr(entidade, field, value)

        try:
            entidade.save(using=db_name)  # Salva a entidade no banco correto
        except IntegrityError as e:
            print(f"[DEBUG] Erro ao atualizar entidade: {e}")
            messages.error(self.request, "Erro ao atualizar entidade. Verifique os dados.")
            return self.form_invalid(form)  

        return super().form_valid(form)




class EntidadeDeleteView(LicenseMixin, DeleteView):
    model = models.Entidades
    template_name = 'entidade_confirm_delete.html'
    success_url = reverse_lazy('entidades')

    def get_object(self, queryset=None):
        db_name = self.get_license().lice_nome if self.get_license() else "default"
        enti_clie = self.kwargs.get("enti_clie")  # Obtenha o enti_clie da URL

        print(f"[DEBUG] Buscando entidade com enti_clie={enti_clie} no banco {db_name}")

        entidade = models.Entidades.objects.using(db_name).filter(enti_clie=enti_clie).first()

        if not entidade:
            raise Http404("Entidade não encontrada.")

        return entidade

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.delete_object(self.object)  # Chama o método delete_object para excluir
        messages.success(request, "Entidade excluída com sucesso!")
        return redirect(self.get_success_url())



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