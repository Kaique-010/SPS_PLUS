from django import forms
from . import models

class Entradas(forms.ModelForm):
    class Meta:    
        model = models.EntradaEstoque
        fields = ['entr_data', 'entr_empr', 'entr_fili', 'entr_prod', 'entr_enti', 'entr_obse', 'entr_tota']
        widgets = {
            'entr_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'entr_enti': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Entidade Responsável'}),
            'entr_prod': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'entr_fili': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira a Filial'}),
            'entr_empr': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Insira a Empresa'}),
            'entr_obse': forms.NumberInput(attrs={'class': 'form-control', 'Placeholder': 'Insira o Documento'}),
            'entr_tota': forms.NumberInput(attrs={'class': 'form-control', 'rows': 3}),
        }
