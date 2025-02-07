from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from sps_plus import settings
from .models import Licencas, Filiais, Empresas
from .forms import LicencasForm, EmpresasForm, FiliaisForm, LoginForm
from .models import Usuarios
from .forms import UsuarioForm

User = get_user_model()

class LicencaLoginView(TemplateView):
    
    template_name = 'licencas/login.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            usua_login = form.cleaned_data['usua_login']
            password = form.cleaned_data['password']
            
            print(f"Tentando autenticar: {usua_login}, senha: {password}")
            
            user = authenticate(request, usua_login=usua_login, password=password)
            
            if user is not None:
                login(request, user)
                print(f"Login realizado com sucesso para o usuário {user.usua_nome}")
                # Alterado para usar 'licenca' em vez de 'license'
                print(f"Licença logada: {request.user.licencas.lice_nome}")
                print(f"Banco conectado: {settings.DATABASES[request.user.licencas.lice_nome]}")       
                return redirect('home')  
            else:
                messages.error(request, "Login ou senha inválidos.")
                print("Erro: Login ou senha inválidos.")
        else:
            messages.error(request, "Formulário inválido.")
        
        return render(request, self.template_name, {'form': form})

def login_view(request):
    # Se o usuário já estiver autenticado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usua_login = form.cleaned_data['usua_login']
            password = form.cleaned_data['password']

            print(f"Tentando autenticar: {usua_login}, senha: {password}")
            user = authenticate(request, usua_login=usua_login, password=password)

            if user:
                login(request, user)  # Faz login do usuário
                request.session.modified = True  # Garante que a sessão foi alterada
                request.session.save()
                print(f"Usuário autenticado na home? {request.user.is_authenticated}")

                # Verifica se a licença do usuário existe
                if hasattr(user, "licenca") and user.licenca:
                    print(f"Licença logada: {user.licenca.lice_nome}")
                    
                    # Verifica se a licença tem um banco de dados associado
                    if user.licenca.lice_nome in settings.DATABASES:
                        print(f"Banco conectado: {settings.DATABASES[user.licenca.lice_nome]}")
                    else:
                        print("⚠️ Banco de dados da licença não configurado corretamente.")

                return redirect('home')  # Redireciona após o login

            else:
                messages.error(request, "Login ou senha inválidos.")  # Mensagem de erro

    else:
        form = LoginForm()  # Cria um formulário vazio para GET

    return render(request, 'licencas/login.html', {'form': form}) 


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

class LicencasListView(ListView):
    model = Licencas
    template_name = "licencas/licencas_list.html"
    context_object_name = "licencas"

    def get_queryset(self):
        queryset = super().get_queryset().order_by('lice_id') 
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
    
    
class LicencasCreateView(CreateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


class LicencasUpdateView(UpdateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


class LicencasDetailView(DetailView):
    model = Licencas
    template_name = "licencas/licencas_detail.html"
    context_object_name = "licenca"



class LicencasDeleteView(DeleteView):
    model = Licencas
    template_name = "licencas/licencas_confirm_delete.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licenca"


class EmpresaListView(ListView):
    model = Empresas
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('empr_nome') 
        nome = self.request.GET.get('empr_nome', '')
        documento = self.request.GET.get('empr_docu', '')

        if nome:
            queryset = queryset.filter(empr_nome__icontains=nome)  

        if documento:
            queryset = queryset.filter(empr_docu__icontains=documento)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empr_nome'] = self.request.GET.get('empr_nome', '')
        context['empr_docu'] = self.request.GET.get('empr_docu', '')
        return context


class EmpresaCreateView(CreateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_create.html'
    success_url = reverse_lazy("empresa_list")

class EmpresaUpdateView(UpdateView):
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
    template_name = 'filial_list.html'
    context_object_name = 'filial'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('fili_id') 
        nome = self.request.GET.get('fili_nome', '')
        documento = self.request.GET.get('fili_docu', '')

        if nome:
            queryset = queryset.filter(fili_nome__icontains=nome)  

        if documento:
            queryset = queryset.filter(fili_docu__icontains=documento)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fili_nome'] = self.request.GET.get('fili_nome', '')
        context['fili_docu'] = self.request.GET.get('fili_docu', '')
        return context

class FilialCreateView(CreateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_create.html'
    success_url = reverse_lazy('filial_list')

class FilialUpdateView(UpdateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_update.html'

class FilialDetailView(DetailView):
    model = Filiais
    template_name = 'licencas/filial_detail.html'

class FilialDeleteView(DeleteView):
    model = Filiais
    template_name = 'licencas/filial_confirm_delete.html'
    success_url = reverse_lazy('filial_list')
    


class UsuarioCreateView(CreateView):
    model = Usuarios
    form_class = UsuarioForm
    template_name = "licencas/usuario_form.html"
    success_url = reverse_lazy("home") 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.set_password(form.cleaned_data["password1"])  
        self.object.save()
        return response