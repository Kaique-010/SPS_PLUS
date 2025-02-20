from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import connections
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from licencas.mixins import LicenseMixin
from .models import Licencas, Filiais, Empresas
from .forms import LicencasForm, EmpresasForm, FiliaisForm, LoginForm
from .models import Usuarios
from .forms import UsuarioForm
class UsuarioLoginView(FormView):
    template_name = "licencas/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)

        if user:
            login(self.request, user)

            # Certifique-se de carregar a licença do usuário corretamente
            licenca = user.licenca if hasattr(user, "licenca") else None
            if licenca:
                licenca = user.licenca  # Se for uma ForeignKey, precisa ser explicitamente recuperada
                banco = licenca.lice_nome  # Nome do banco

                print(f"Licença: {licenca}, Nome do banco: {banco}, Tipo: {type(banco)}")
                print(f"🎯 Banco salvo na sessão: {banco}")

                self.request.session["id"] = user.id 
                self.request.session["licenca_nome"] = banco  # Salvar na sessão
                
            return super().form_valid(form)

        return self.form_invalid(form)



def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirecionar para a página correta com base na licença
            if 'licenca_id' in request.session:
                return redirect('empresas')  # ou outra URL que você deseja
            else:
                return redirect('select_license')  # Se a licença não estiver selecionada
        else:
            # Login inválido
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    
    return render(request, 'login.html')


def select_license(request):
    if request.method == "POST":
        # Obtemos o nome da licença selecionada
        licenca_nome = request.POST.get('lice_nome')
        print("Licença selecionada:", licenca_nome)  # Verifique o valor
        
        try:
            # Buscamos a licença pelo nome
            licenca = Licencas.objects.get(lice_nome=licenca_nome)
            request.session['selected_licenca_nome'] = licenca.lice_nome  # Armazenamos o nome da licença na sessão

            # Verifica se o usuário está autenticado
            if request.user.is_authenticated:
                print("Usuário autenticado com licença selecionada!")
            else:
                print("Usuário não autenticado")

            return redirect('home')

        except Licencas.DoesNotExist:
            print("Licença não encontrada!")
            return redirect('select-license')  # Ou página de erro

    return render(request, 'licencas/select_license.html', {'licencas': Licencas.objects.all()})





@login_required
def select_database(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        selected_db = request.POST.get('db_name')
        if selected_db:
            request.session['selected_db'] = selected_db
            return redirect('home')
    
    # Lista dos bancos disponíveis (você pode carregar do JSON ou do seu modelo)
    available_dbs = ['save1', 'origin', 'TESTES 2']  
    return render(request, 'select_database.html', {'databases': available_dbs})



@login_required
def select_company_branch(request):
    # Apenas usuários não superusuários devem acessar essa rota
    if request.user.is_superuser:
        return redirect('home')
    
    # Supondo que o usuário tenha acesso à licença, obtenha as empresas associadas a essa licença
    licenca = request.user.licenca
    empresas = Empresas.objects.filter(licenca=licenca)
    
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        filial_id = request.POST.get('filial')
        if empresa_id and filial_id:
            request.session['selected_empresa'] = empresa_id
            request.session['selected_filial'] = filial_id
            return redirect('home')
    
    context = {
        'empresas': empresas,
        # Você pode, opcionalmente, carregar as filiais do primeiro registro ou usar JavaScript para
        # carregar dinamicamente as filiais conforme a seleção da empresa.
    }
    return render(request, 'licencas/select_company_branch.html', context)

class LicencasListView(LicenseMixin, ListView):
    model = Licencas
    template_name = "licencas/licencas_list.html"
    context_object_name = "licencas"

    def get_queryset(self):
        self.set_db()  # Certifica que estamos no banco correto antes da consulta
        queryset = super().get_queryset().using(self.db_name).order_by('lice_id')  # Use o banco correto

        nome = self.request.GET.get('lice_nome', '')
        lice_id = self.request.GET.get('lice_id', '')

        if nome:
            queryset = queryset.filter(lice_nome__icontains=nome)

        if lice_id:
            try:
                queryset = queryset.filter(lice_id=int(lice_id))
            except ValueError:
                pass

        return queryset
    
    
class LicencasCreateView(LicenseMixin,CreateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


class LicencasUpdateView(LicenseMixin,UpdateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


class LicencasDetailView(LicenseMixin,DetailView):
    model = Licencas
    template_name = "licencas/licencas_detail.html"
    context_object_name = "licenca"



class LicencasDeleteView(LicenseMixin,DeleteView):
    model = Licencas
    template_name = "licencas/licencas_confirm_delete.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licenca"


class EmpresaListView(LicenseMixin, ListView):
    model = Empresas
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'

    def dispatch(self, request, *args, **kwargs):
        if 'licenca_id' not in request.session:
            return redirect('select_license')  # Redireciona se não houver licença selecionada
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('empr_nome')
        nome = self.request.GET.get('empr_nome', '')
        documento = self.request.GET.get('empr_docu', '')

        if nome:
            queryset = queryset.filter(empr_nome__icontains=nome)

        if documento:
            queryset = queryset.filter(empr_docu__icontains=documento)

        return queryset.filter(licenca=self.get_license()).order_by('empr_nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empr_nome'] = self.request.GET.get('empr_nome', '')
        context['empr_docu'] = self.request.GET.get('empr_docu', '')
        return context


class EmpresaCreateView(LicenseMixin, CreateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_create.html'
    success_url = reverse_lazy("empresa_list")
    
class EmpresaUpdateView(LicenseMixin, UpdateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_update.html'
    

class EmpresaDetailView(DetailView):
    model = Empresas
    template_name = 'licencas/empresa_detail.html'

class EmpresaDeleteView(DeleteView):
    model = Empresas
    template_name = 'licencas/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa_list')
    


class FilialListView(ListView):
    model = Filiais
    template_name = 'filiais/filial_list.html'  # Ajuste conforme seu template
    context_object_name = 'filiais'

    def get_queryset(self):
        # Obtém a licença do usuário atual
        user = self.request.user
        if user.is_authenticated:
            return Filiais.objects.filter(empresa__licenca=user.licenca).distinct()
        return Filiais.objects.none()

   
class FilialCreateView(LicenseMixin, CreateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_create.html'
    success_url = reverse_lazy('filial_list')
    
    def form_valid(self, form):

        empresa = self.request.user.empresas.first() 
        form.instance.empresa = empresa
        return super().form_valid(form)
    
class FilialUpdateView(LicenseMixin, UpdateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_update.html'
    
    def form_valid(self, form):
        form.instance.licenca = self.get_license() 
        return super().form_valid(form)

class FilialDetailView(DetailView):
    model = Filiais
    template_name = 'licencas/filial_detail.html'

class FilialDeleteView(DeleteView):
    model = Filiais
    template_name = 'licencas/filial_confirm_delete.html'
    success_url = reverse_lazy('filial_list')
    


class UsuarioCreateView(LicenseMixin,CreateView):
    model = Usuarios
    form_class = UsuarioForm
    template_name = "licencas/usuario_form.html"
    success_url = reverse_lazy("usuarios_list") 


    def form_valid(self, form):
        form.instance.licenca = self.get_license()  # Certifica-se de que a licença está definida
        return super().form_valid(form)

class UsuariosListView(LicenseMixin,ListView):
    model = Usuarios
    template_name = 'licencas/usuarios_list.html'
    context_object_name = 'usuarios'
    

def test_session(request):
    # Salva dados simples na sessão
    request.session['test_key'] = 'test_value'
    request.session.save()  # Salva explicitamente
    return HttpResponse(f"Test session saved: {request.session['test_key']}")