from django import forms
from .models import Licencas, Usuarios, Empresas, Filiais
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class LicencasForm(forms.ModelForm):
    lice_docu = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF'})
    )
    lice_nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'})
    )

    class Meta:
        model = Licencas
        exclude = ['lice_data_cria']
        fields = ['lice_docu', 'lice_nome', 'lice_emai', 'lice_bloq', 'lice_data_cria']
        widgets = {
            'lice_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'lice_bloq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lice_data_cria': forms.DateInput(attrs={'class': 'form-control'}),
        }

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['empr_nome', 'empr_docu', 'empr_ie', 'empr_cep', 'empr_ende', 'empr_nume', 'empr_cida', 'empr_esta', 'empr_bair', 'empr_emai']
        widgets = {
            'empr_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'empr_docu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF', 'maxlength': '14'}),
            'empr_ie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'empr_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'}),
            'empr_ende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'empr_nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'empr_cida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'empr_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '2'}),
            'empr_bair': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro', 'maxlength': '100'}),
            'empr_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }
        
    


class FiliaisForm(forms.ModelForm):
    class Meta:
        model = Filiais
        fields = ['empr_codi','empr_nome', 'empr_docu', 'empr_ie', 'empr_cep', 'empr_ende', 'empr_nume', 'empr_cida', 'empr_esta', 'empr_bair', 'empr_emai']
        widgets = {
            'empr_codi': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Id da Empresa'}),
            'empr_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'empr_docu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF', 'maxlength': '14'}),
            'empr_ie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'empr_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'}),
            'empr_ende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'empr_nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'empr_cida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'empr_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '2'}),
            'empr_bair': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro', 'maxlength': '100'}),
            'empr_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ["nome", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalização dos widgets para melhorar a experiência do usuário
        #self.fields["usuario_id"].widget.attrs.update({"class": "form-control", "placeholder": "Nome Completo"})
        self.fields["nome"].widget.attrs.update({"class": "form-control", "placeholder": "Nome Completo"}),
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Senha"})

    def save(self, commit=True):
        user = super().save(commit=False)
        # Salva em texto puro no campo legado (password -> usua_senh_mobi)
        pwd = self.cleaned_data.get("password1") or self.cleaned_data.get("password") or ""
        user.password = pwd
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    lice_docu = forms.CharField(
        label="Documento",
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF'})
    )
    username = forms.CharField(
        label="Login",
        max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            return username.strip()
        return username

    def clean_lice_docu(self):
        doc = self.cleaned_data.get("lice_docu")
        if doc:
            return doc.replace(".", "").replace("-", "").replace("/", "").strip()
        return doc

    def clean(self):
        # NÃO chamar o AuthenticationForm.clean padrão para evitar autenticar sem lice_docu
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        lice_docu = self.cleaned_data.get("lice_docu")

        if username and password:
            user = authenticate(self.request, username=username, password=password, lice_docu=lice_docu)
            if user is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(user)
            self.user_cache = user
        return self.cleaned_data


class UsuarioCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Usuarios
        fields = ('nome', 'email', 'password1', 'password2') 

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user