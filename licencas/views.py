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
from licencas.mixins import LicenseDatabaseMixin
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
                # Salva as configurações do banco de dados na sessão
                self.request.session["test_key"] = "test_value"
                self.request.session["db_config"] = licenca.db_config
                self.request.session["licenca_lice_nome"] = licenca.lice_nome
                self.request.session.modified = True
                print(f"Licença salva na sessão: {licenca.lice_nome}")

                # Força a sessão a ser salva
                self.request.session.save()
                print(f"🎯 Banco salvo na sessão: {licenca.lice_nome}")
            else:
                print("🚨 Erro: Usuário não possui uma licença ou banco de dados configurado.")

            return super().form_valid(form)

        return self.form_invalid(form)




class LicencasListView(LicenseDatabaseMixin, ListView):
    model = Licencas
    template_name = "licencas/licencas_list.html"
    context_object_name = "licencas"


from django.db import transaction

from django.contrib import messages

class LicencasCreateView(LicenseDatabaseMixin,CreateView):
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






class LicencasUpdateView(LicenseDatabaseMixin,UpdateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licencas"


class LicencasDetailView(LicenseDatabaseMixin,DetailView):
    model = Licencas
    template_name = "licencas/licencas_detail.html"
    context_object_name = "licenca"



class LicencasDeleteView(LicenseDatabaseMixin,DeleteView):
    model = Licencas
    template_name = "licencas/licencas_confirm_delete.html"
    success_url = reverse_lazy("licenca_list")
    context_object_name = "licenca"


class EmpresaListView(LicenseDatabaseMixin, ListView):
    model = Empresas
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'
    
    
    def get_queryset(self):
        # Filtra as filiais pela empresa do usuário
        user = self.request.user
        return Filiais.objects.filter(empresa__in=user.empresas.all())

    

class EmpresaCreateView(LicenseDatabaseMixin, CreateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_create.html'
    success_url = reverse_lazy("empresa_list")
    
class EmpresaUpdateView(LicenseDatabaseMixin, UpdateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_update.html'
    

class EmpresaDetailView(LicenseDatabaseMixin,DetailView):
    model = Empresas
    template_name = 'licencas/empresa_detail.html'

class EmpresaDeleteView(LicenseDatabaseMixin,DeleteView):
    model = Empresas
    template_name = 'licencas/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa_list')
    


class FilialListView(LicenseDatabaseMixin,ListView):
    model = Filiais
    template_name = 'filiais/filial_list.html'  # Ajuste conforme seu template
    context_object_name = 'filiais'

    def get_queryset(self):
        # Filtra as filiais pela empresa do usuário
        user = self.request.user
        return Filiais.objects.filter(empresa__in=user.empresas.all())

   
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

class FilialDeleteView(LicenseDatabaseMixin,DeleteView):
    model = Filiais
    template_name = 'licencas/filial_confirm_delete.html'
    success_url = reverse_lazy('filial_list')
    


class UsuarioCreateView(LicenseDatabaseMixin,CreateView):
    model = Usuarios
    form_class = UsuarioForm
    template_name = "licencas/usuario_form.html"
    success_url = reverse_lazy("usuarios_list") 


    def form_valid(self, form):
        form.instance.licenca = self.get_license()  # Certifica-se de que a licença está definida
        return super().form_valid(form)

class UsuariosListView(LicenseDatabaseMixin,ListView):
    model = Usuarios
    template_name = 'licencas/usuarios_list.html'
    context_object_name = 'usuarios'
    

def test_session(request):
    # Salva dados simples na sessão
    request.session['test_key'] = 'test_value'
    request.session.save()  # Salva explicitamente
    return HttpResponse(f"Test session saved: {request.session['test_key']}")