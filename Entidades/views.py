from io import BytesIO
from django.forms import ValidationError
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
import openpyxl
from django.contrib import messages
from django.db import connection
from django.urls import reverse_lazy
import requests
from .models import Entidades
from django.db.models import Max
from .serializers import EntidadesSerializer
from .forms import EntidadesForm 
from rest_framework import viewsets
from rest_framework import filters
from django.core.paginator import Paginator
from Entidades import models


class EntidadesViewSet(viewsets.ModelViewSet):
    queryset = Entidades.objects.filter(enti_empr=1)
    serializer_class = EntidadesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']
    
    

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
class EntidadesListView(ListView):
    model = Entidades
    template_name = 'entidades.html'
    context_object_name = 'entidades'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id') 
        nome = self.request.GET.get('enti_nome')
        enti_clie = self.request.GET.get('enti_clie')

        if nome:
            queryset = queryset.filter(enti_nome__icontains=nome) 

        if enti_clie:
            queryset = queryset.filter(enti_clie=enti_clie)
           
        return queryset





class EntidadeCreateView(CreateView):
    model = models.Entidades
    form_class = EntidadesForm
    template_name = 'entidade_form.html'
    success_url = reverse_lazy('entidades')  

    def form_valid(self, form):
        return super().form_valid(form)




def entidade_update(request, pk):
    entidade = get_object_or_404(Entidades, pk=pk)
    
    if request.method == 'POST':
        form = EntidadesForm(request.POST, instance=entidade)
        if form.is_valid():
            form.save()
            messages.success(request, "Entidade salva com sucesso!")
            return redirect('entidades')  
        else:
            print("Formulário inválido:", form.errors) 
    else:
        form = EntidadesForm(instance=entidade)
    
    return render(request, 'entidade_form.html', {'form': form})



def entidade_delete(request, pk):
    entidade = get_object_or_404(Entidades, pk=pk)
    if request.method == 'POST':
        entidade.delete()
        return redirect('entidades')
    messages.success(request, "Entidade excluida com sucesso!")
    return render(request, 'entidade_confirm_delete.html', {'entidade': entidade})


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