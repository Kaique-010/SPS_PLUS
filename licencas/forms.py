from django import forms
from .models import Licencas, Usuarios, Empresas, Filiais


class LicencasForm(forms.ModelForm):
    class Meta:
        model = Licencas
        fields = ['lice_docu', 'lice_nome', 'lice_emai', 'lice_bloq']
        widgets = {
            'lice_docu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ/CPF'}),
            'lice_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'lice_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'lice_bloq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['usua_nome', 'usua_login', 'usua_data_nasc', 'usua_sexo', 'usua_emai', 'usua_fone', 'usua_senh', 'usua_bloq', 'licenca']
        widgets = {
            'usua_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'usua_login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}),
            'usua_data_nasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usua_sexo': forms.Select(attrs={'class': 'form-select'}),
            'usua_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'usua_fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'usua_senh': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'usua_bloq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'licenca': forms.Select(attrs={'class': 'form-select'}),
        }


class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['empr_nome', 'licenca']
        widgets = {
            'empr_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'licenca': forms.Select(attrs={'class': 'form-select'}),
        }


class FiliaisForm(forms.ModelForm):
    class Meta:
        model = Filiais
        fields = ['fili_nome', 'empresa']
        widgets = {
            'fili_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Filial'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
        }
