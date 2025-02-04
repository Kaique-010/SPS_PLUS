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
            'usua_sexo': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Selecione...'), ('M', 'Masculino'), ('F', 'Feminino')]),
            'usua_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'usua_fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'usua_senh': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha', 'type': 'password'}),
            'usua_bloq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'licenca': forms.Select(attrs={'class': 'form-select'}),
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
            'empr_bair': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '100'}),
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
