from django import forms
from .models import Licencas, Usuarios, Empresas, Filiais
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


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
        fields = ['empr_nome', 'licenca', 'empr_docu', 'empr_ie', 'empr_cep', 'empr_ende', 'empr_nume', 'empr_cida', 'empr_esta', 'empr_bair', 'empr_emai']
        widgets = {
            'empr_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'licenca': forms.Select(attrs={'class': 'form-select'}),
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
        fields = ['fili_nome', 'empresa','fili_docu', 'fili_ie', 'fili_cep', 'fili_ende', 'fili_nume', 'fili_cida', 'fili_esta', 'fili_bair', 'fili_emai']
        widgets = {
            'fili_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Filial'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'fili_docu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF', 'maxlength': '14'}),
            'fili_ie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'fili_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'}),
            'fili_ende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'fili_nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'fili_cida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'fili_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '2'}),
            'fili_bair': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '100'}),
            'fili_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ["licenca", "nome", "login", "data_nascimento", "sexo", 
                  "email", "telefone", "ativo", "empresas", "filiais", "is_staff"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalização dos widgets para melhorar a experiência do usuário
        #self.fields["usuario_id"].widget.attrs.update({"class": "form-control", "placeholder": "Nome Completo"})
        self.fields["licenca"].widget.attrs.update({"class": "form-select", "placeholder": "Licença"})
        self.fields["nome"].widget.attrs.update({"class": "form-control", "placeholder": "Nome Completo"})
        self.fields["login"].widget.attrs.update({"class": "form-control", "placeholder": "Login"})
        self.fields["data_nascimento"].widget.attrs.update({"class": "form-control", "type": "date"})
        self.fields["sexo"].widget.attrs.update({"class": "form-select"})
        self.fields["empresas"].widget.attrs.update({"class": "form-select"})
        self.fields["filiais"].widget.attrs.update({"class": "form-select"})
        self.fields["is_staff"].widget.attrs.update({"class": "form-check-input"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "E-mail"})
        self.fields["telefone"].widget.attrs.update({"class": "form-control", "placeholder": "Telefone"})

        # Checkbox personalizado para os campos booleanos
        self.fields["ativo"].widget.attrs.update({"class": "form-check-input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
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


class UsuarioCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Usuarios
        fields = ('login', 'nome', 'email', 'password1', 'password2')  # Ajuste para 'login' no lugar de 'usua_login'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user