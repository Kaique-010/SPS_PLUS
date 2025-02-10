from django import forms
from . import models
from produto.models import SaldoProduto
from django.core.exceptions import ValidationError

class Saidas(forms.ModelForm):
    class Meta:
        model = models.Saida_Produtos
        fields = ['data', 'entidade', 'prod_codi', 'quantidade', 'documento', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'entidade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Entidade Responsável'}),
            'prod_codi': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira a Quantidade'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Documento se Necessário'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        prod_codi = self.cleaned_data.get('prod_codi')  

        if prod_codi is None:  
            raise forms.ValidationError("O produto deve ser selecionado.")

       
        return quantidade
