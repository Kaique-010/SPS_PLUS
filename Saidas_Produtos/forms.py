from django import forms
from . import models
from produto.models import SaldoProduto
from django.core.exceptions import ValidationError

class Saidas(forms.ModelForm):
    class Meta:    
        model = models.SaidasEstoque
        fields = ['said_data', 'said_empr', 'said_fili', 'said_prod', 'said_enti', 'said_obse', 'said_tota']
        widgets = {
            'said_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'said_enti': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Entidade Responsável'}),
            'said_prod': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'said_fili': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira a Filial'}),
            'said_empr': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Insira a Empresa'}),
            'said_obse': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Insira o Documento'}),
            'said_tota': forms.NumberInput(attrs={'class': 'form-control', 'rows': 3}),
        }


    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        prod_codi = self.cleaned_data.get('prod_codi')  

        if prod_codi is None:  
            raise forms.ValidationError("O produto deve ser selecionado.")

       
        return quantidade
