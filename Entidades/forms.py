from django import forms
from .models import Entidades

class EntidadesForm(forms.ModelForm):
    class Meta:
        model = Entidades
        fields = [
            'enti_empr', 'enti_clie', 'enti_nome','enti_tipo_enti', 'enti_fant', 'enti_cpf', 'enti_cnpj', 
            'enti_insc_esta', 'enti_cep', 'enti_ende', 'enti_nume', 
            'enti_cida', 'enti_esta', 'enti_fone', 'enti_celu', 
            'enti_emai', 'enti_emai_empr'
        ]
        widgets = {
            'enti_empr': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'enti_clie': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cliente'}),
            'enti_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'enti_tipo_enti': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Classificação Entidade'}),
            'enti_fant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Fantasia'}),
            'enti_cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF', 'maxlength': '11'}),
            'enti_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'maxlength': '14'}),
            'enti_insc_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'enti_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'}),
            'enti_ende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'enti_nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'enti_cida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'enti_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '2'}),
            'enti_fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'maxlength': '14'}),
            'enti_celu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'maxlength': '15'}),
            'enti_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Pessoal'}),
            'enti_emai_empr': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email da Empresa'}),
        }

    def __init__(self, *args, **kwargs):
        super(EntidadesForm, self).__init__(*args, **kwargs)
        # Torne esses campos não obrigatórios se necessário
        self.fields['enti_cpf'].required = False
        self.fields['enti_cnpj'].required = False
        self.fields['enti_fone'].required = False
        self.fields['enti_emai'].required = False
        self.fields['enti_emai_empr'].required = False  
        self.fields['enti_insc_esta'].required = False 
        self.fields['enti_empr'].required = False 
        self.fields['enti_fant'].required = False 
        self.fields['enti_ende'].required = False 
        self.fields['enti_cida'].required = False
        self.fields['enti_esta'].required = False
        self.fields['enti_clie'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('enti_cpf')
        cnpj = cleaned_data.get('enti_cnpj')
        ie = cleaned_data.get('enti_insc_esta')

        # Verificação de CPF não coexistir com CNPJ ou IE
        if cpf and (cnpj or ie):
            raise forms.ValidationError("Se o CPF for fornecido, CNPJ e Inscrição Estadual não devem ser preenchidos.")
        
        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk is None:  
            ultimo_codigo = Entidades.objects.all().order_by('-enti_clie').first()
            if ultimo_codigo:
                instance.enti_clie = ultimo_codigo.enti_clie + 1
            else:
                instance.enti_clie = 1  # Caso não haja registros ainda
        if commit:
            instance.save()
        return instance
