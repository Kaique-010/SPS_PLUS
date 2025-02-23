from urllib import request
from django.conf import settings
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

from licencas.db_router import LicenseDatabaseManager
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

        # Autentica o usuário
        user = authenticate(self.request, username=username, password=password)

        if user:
            login(self.request, user)

            # Obtém a licença do usuário
            licenca = getattr(user, "licenca", None)
            if licenca and licenca.db_config:
                
                self.request.session["db_config"] = licenca.db_config
                self.request.session["licenca_lice_nome"] = licenca.lice_nome
                self.request.session.modified = True
                print(f"Licença salva na sessão: {licenca.lice_nome}")

      
            else:
                print("🚨 Erro: Usuário não possui uma licença ou banco de dados configurado.")

            return super().form_valid(form)

        return self.form_invalid(form)



@method_decorator(login_required, name='dispatch')
class LicencasListView( ListView):
    model = Licencas
    template_name = "licencas/licencas_list.html"
    context_object_name = "licencas"

    
    def get_queryset(self):
        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:
            return self.request.user.empresas.all()
        else:
            return Empresas.objects.none()

from django.db import transaction

from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class LicencasCreateView(CreateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")

    def form_valid(self, form):
        lice_docu = form.cleaned_data.get('lice_docu')

        if Licencas.objects.filter(lice_docu=lice_docu).exists():
            form.add_error('lice_docu', 'Licença com este Documento já existe.')
            return self.form_invalid(form)

        print("Formulário válido, preparando para salvar...") 
        licenca = form.save(commit=False)
        print(f"Dados da licença: {licenca}")

        # Preenche o campo db_config manualmente
        licenca.db_config = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": licenca.lice_nome,  # Nome do banco de dados
            "USER": "postgres",
            "PASSWORD": "@spartacus201@",
            "HOST": "localhost",
            "PORT": "5432",
            "TIME_ZONE": "America/Sao_Paulo",
            "CONN_MAX_AGE": 600,
            "ATOMIC_REQUESTS": True,
            "CONN_HEALTH_CHECKS": True,
            "OPTIONS": {}
        }

        try:
            licenca.save()
            print(f"Licença {licenca.lice_nome} salva com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar licença: {str(e)}")
            return self.form_invalid(form)

        LicenseDatabaseManager.ensure_database_exists(licenca)

        db_name = licenca.lice_nome

        superuser_email = form.cleaned_data.get('lice_emai')
        superuser_password = 'roma3030@'
        superuser_name = 'admin'  # Usando o nome como login

        try:
            with transaction.atomic(using=db_name):
                superuser = Usuarios.objects.create_superuser(
                    login=superuser_name,  # Agora o login é o nome
                    nome=superuser_name,
                    email=superuser_email,
                    password=superuser_password,
                    licenca=licenca,
                    is_staff=True,
                    is_superuser=True
                )
                print("Superusuário criado com sucesso!")

                # Adicionando mensagem de sucesso
                messages.success(self.request, f"Superusuário {superuser_name} criado com sucesso! Senha: {superuser_password}")

        except Exception as e:
            messages.error(self.request, f"Erro ao criar superusuário: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Formulário inválido:", form.errors)
        return super().form_invalid(form)


def using_db(db_name):
    """
    Context manager para garantir que operações sejam feitas no banco de dados correto.
    """
    connection = connections[db_name]
    with connection.cursor() as cursor:
        yield cursor






@method_decorator(login_required, name='dispatch')
class LicencasUpdateView(UpdateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


@method_decorator(login_required, name='dispatch')
class LicencasDetailView(DetailView):
    model = Licencas
    template_name = "licencas/licencas_detail.html"
    context_object_name = "licenca"


@method_decorator(login_required, name='dispatch')
class LicencasDeleteView(DeleteView):
    model = Licencas
    template_name = "licencas/licencas_confirm_delete.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licenca"
    



@method_decorator(login_required, name='dispatch')
class EmpresaListView(ListView):
    model = Empresas
    template_name = 'empresas/list.html'
    context_object_name = 'empresas'

    
    def get_queryset(self):
        user_licenca = self.request.user.licenca
        db_name = user_licenca.lice_nome if user_licenca else "default"

        queryset = Empresas.objects.using(db_name)  # Utiliza o banco correto para a consulta
        empresas = self.request.GET.get('empr_nome')

        if empresas:
            queryset = queryset.filter(empr_nome__empr_nome__icontains=empresas)

        return queryset
    
    
@method_decorator(login_required, name='dispatch')
class EmpresaCreateView(CreateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_create.html'
    success_url = reverse_lazy("empresa_list")
    
    def form_valid(self, form):
        db_name = getattr(self.request, "db_alias", "default")  # Obtém o banco da requisição
        
        if db_name == "default":
            print("⚠️ Erro: Nenhum banco de dados específico foi definido. Usando default.")
            return self.form_invalid(form)  # Impede salvar no default por erro

        form.instance._state.db = db_name  # Salva a empresa no banco correto
        print(f"✅ Salvando empresa no banco: {db_name}")  # Log para depuração

        return super().form_valid(form)




@method_decorator(login_required, name='dispatch')
class EmpresaUpdateView( UpdateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_update.html'
    
    def get_queryset(self):
        # Filtra o objeto no banco de dados correto
        return Empresas.objects.using(self.request.db_alias).all()

    def form_valid(self, form):
        # Salva as alterações no banco de dados correto
        form.instance.save(using=self.request.db_alias)
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EmpresaDetailView(DetailView):
    model = Empresas
    template_name = 'licencas/empresa_detail.html'
    
    def get_queryset(self):
        # Filtra o objeto no banco de dados correto
        return Empresas.objects.using(self.request.db_alias).all()


@method_decorator(login_required, name='dispatch')
class EmpresaDeleteView(DeleteView):
    model = Empresas
    template_name = 'licencas/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa_list')
    
    def get_queryset(self):
        # Filtra o objeto no banco de dados correto
        return Empresas.objects.using(self.request.db_alias).all()

    def delete(self, request, *args, **kwargs):
        # Exclui o objeto do banco de dados correto
        self.object = self.get_object()
        self.object.delete(using=self.request.db_alias)
        return super().delete(request, *args, **kwargs)
    

class FilialListView(ListView):
    model = Filiais
    template_name = 'filiais/filial_list.html'  # Ajuste conforme seu template
    context_object_name = 'filiais'

    def get_queryset(self):
        user_licenca = self.request.user.licenca
        db_name = user_licenca.lice_nome if user_licenca else "default"

        queryset = Filiais.objects.using(db_name)
        filiais = self.request.GET.get('empr_nome')

        if filiais:
            queryset = queryset.filter(empr_nome__icontains=filiais)

        print(queryset.query)  # Exibe a consulta SQL gerada

        return queryset



   
class FilialCreateView(CreateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_create.html'
    success_url = reverse_lazy('filial_list')
    
    def form_valid(self, form):
         with transaction.atomic():
            db_name = getattr(self.request, "db_alias", "default")  # Obtém o banco da requisição
            
            if db_name == "default":
                print("⚠️ Erro: Nenhum banco de dados específico foi definido. Usando default.")
                return self.form_invalid(form)  # Impede salvar no default por erro

            form.instance._state.db = db_name  # Salva a empresa no banco correto
            print(f"✅ Salvando empresa no banco: {db_name}")  # Log para depuração

            return super().form_valid(form)


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
    success_url = reverse_lazy("usuarios_list") 


    def form_valid(self, form):
        form.instance.licenca = self.get_license()  # Certifica-se de que a licença está definida
        return super().form_valid(form)

class UsuariosListView(ListView):
    model = Usuarios
    template_name = 'licencas/usuarios_list.html'
    context_object_name = 'usuarios'
    

def test_session(request):
    # Salva dados simples na sessão
    request.session['test_key'] = 'test_value'
    request.session.save()  # Salva explicitamente
    return HttpResponse(f"Test session saved: {request.session['test_key']}")