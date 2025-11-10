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

from .models import Licencas, Filiais, Empresas
from licencas.utils import current_alias
from .forms import LicencasForm, EmpresasForm, FiliaisForm, LoginForm
from .models import Usuarios
from .forms import UsuarioForm


class UsuarioLoginView(LoginView):
    template_name = "licencas/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # O LoginView já chama login() com form.get_user(). Aqui apenas
        # garantimos a configuração da sessão (slug/banco) pós-autenticação.
        response = super().form_valid(form)

        user = form.get_user()
        lice_docu = form.cleaned_data.get("lice_docu")

        if user:
            if lice_docu:
                from licencas.utils.licencas_loader import carregar_licencas_dict
                doc = str(lice_docu).replace(".", "").replace("-", "").replace("/", "").strip()
                by_doc = {x["cnpj"]: x for x in carregar_licencas_dict()}
                info = by_doc.get(doc)
                if info:
                    self.request.session["licenca_lice_nome"] = info["slug"]
                    self.request.session["banco_usuario"] = info["db_name"]
                    self.request.session.modified = True
                    try:
                        self.request.session.save()
                    except Exception:
                        pass
                    print(f"Sessão configurada via documento: slug={info['slug']} banco={info['db_name']}")
            else:
                alias = getattr(user._state, 'db', None) or getattr(user, '_auth_db_alias', None)
                if alias and alias.startswith('cliente_'):
                    slug = alias.replace('cliente_', '')
                    db_name = getattr(user, '_cliente_db_name', None)
                    self.request.session["licenca_lice_nome"] = slug
                    if db_name:
                        self.request.session["banco_usuario"] = db_name
                    self.request.session.modified = True
                    try:
                        self.request.session.save()
                    except Exception:
                        pass
                    print(f"Sessão configurada via alias: slug={slug} banco={db_name}")
                else:
                    print("Aviso: sessão sem slug configurado; seguindo com padrão.")

        return response

    def get_success_url(self):
        # Honra ?next=/home/ se presente; caso contrário, fallback para 'home'
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        return reverse_lazy("home")



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

        try:
            licenca.save()
            print(f"Licença {licenca.lice_nome} salva com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar licença: {str(e)}")
            return self.form_invalid(form)

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
        alias = current_alias(self.request)
        queryset = Empresas.objects.using(alias)
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
        db_name = current_alias(self.request)
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
        alias = current_alias(self.request)
        return Empresas.objects.using(alias).all()

    def form_valid(self, form):
        alias = current_alias(self.request)
        form.instance.save(using=alias)
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EmpresaDetailView(DetailView):
    model = Empresas
    template_name = 'licencas/empresa_detail.html'
    
    def get_queryset(self):
        alias = current_alias(self.request)
        return Empresas.objects.using(alias).all()


@method_decorator(login_required, name='dispatch')
class EmpresaDeleteView(DeleteView):
    model = Empresas
    template_name = 'licencas/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa_list')
    
    def get_queryset(self):
        alias = current_alias(self.request)
        return Empresas.objects.using(alias).all()

    def delete(self, request, *args, **kwargs):
        alias = current_alias(request)
        self.object = self.get_object()
        self.object.delete(using=alias)
        return super().delete(request, *args, **kwargs)
    

class FilialListView(ListView):
    model = Filiais
    template_name = 'filiais/filial_list.html'  # Ajuste conforme seu template
    context_object_name = 'filiais'

    def get_queryset(self):
        alias = current_alias(self.request)
        queryset = Filiais.objects.using(alias)
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
            db_name = current_alias(self.request)
            if db_name == "default":
                print("⚠️ Erro: Nenhum banco de dados específico foi definido. Usando default.")
                return self.form_invalid(form)
            form.instance._state.db = db_name
            print(f"✅ Salvando empresa no banco: {db_name}")
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