from django import forms
from .models import Licencas, Usuarios, Empresas, Filiais
from django.contrib.auth.forms import UserCreationForm


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
        fields = ["usua_nome", "usua_login", "usua_emai", "usua_fone", "usua_data_nasc", "usua_sexo", 
                  "licenca", "empresas", "filiais", "usua_bloq", "usua_libe_clie_bloq", "usua_libe_pedi_comp"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalização dos widgets para melhorar a experiência do usuário
        self.fields["usua_nome"].widget.attrs.update({"class": "form-control", "placeholder": "Nome Completo"})
        self.fields["usua_login"].widget.attrs.update({"class": "form-control", "placeholder": "Login"})
        self.fields["usua_emai"].widget.attrs.update({"class": "form-control", "placeholder": "E-mail"})
        self.fields["usua_fone"].widget.attrs.update({"class": "form-control", "placeholder": "Telefone"})
        self.fields["usua_data_nasc"].widget.attrs.update({"class": "form-control", "type": "date"})
        self.fields["usua_sexo"].widget.attrs.update({"class": "form-select"})
        self.fields["licenca"].widget.attrs.update({"class": "form-control"})
        self.fields["empresas"].widget.attrs.update({"class": "form-control"})
        self.fields["filiais"].widget.attrs.update({"class": "form-control"})

        # Checkbox personalizado para os campos booleanos
        self.fields["usua_bloq"].widget.attrs.update({"class": "form-check-input"})
        self.fields["usua_libe_clie_bloq"].widget.attrs.update({"class": "form-check-input"})
        self.fields["usua_libe_pedi_comp"].widget.attrs.update({"class": "form-check-input"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"]) 
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    documento = forms.CharField(
        label="CPF/CNPJ", 
        max_length=14, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF/CNPJ'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )
