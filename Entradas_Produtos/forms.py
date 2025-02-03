from django import forms
from . import models

class Entradas(forms.ModelForm):
    class Meta:    
        model = models.Entrada_Produtos
        fields = ['data', 'entidade', 'produto_codigo', 'quantidade', 'documento', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'entidade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Entidade Responsável'}),
            'produto_codigo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira a Quantidade'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Documento se Necessário'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
