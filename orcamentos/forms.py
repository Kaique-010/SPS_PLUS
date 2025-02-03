from django import forms
from .models import Orcamento, OrcamentoPecas
from django.forms import inlineformset_factory

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            'orca_empr', 'orca_fili', 'orca_codi', 'orca_aber', 'orca_enti',
            'orca_vend', 'orca_cond', 'orca_resp', 'orca_tipo_fret', 'orca_vali',
            'orca_tipo_impo', 'orca_praz_entr', 'orca_obse', 'orca_valo_fret',
            'orca_valo_outr', 'orca_valo_desc', 'orca_valo_tota'
        ]
        widgets = {
            'orca_empr': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'orca_fili': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Filial'}),
            'orca_codi': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Código do orçamento'}),
            'orca_aber': forms.DateInput(attrs={'class': 'form-control',  'type': 'date'}, format='%Y-%m-%d'),
            'orca_enti': forms.Select(attrs={'class': 'form-control'}),
            'orca_vend': forms.Select(attrs={'class': 'form-control'}),
            'orca_cond': forms.NumberInput(attrs={'class': 'form-control'}),
            'orca_resp': forms.NumberInput(attrs={'class': 'form-control'}),
            'orca_tipo_fret': forms.NumberInput(attrs={'class': 'form-control'}),
            'orca_vali': forms.DateInput(attrs={'class': 'form-control',  'type': 'date'}, format='%Y-%m-%d'),
            'orca_tipo_impo': forms.TextInput(attrs={'class': 'form-control'}),
            'orca_praz_entr': forms.TextInput(attrs={'class': 'form-control'}),
            'orca_obse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'orca_valo_fret': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'orca_valo_outr': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'orca_valo_desc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'orca_valo_tota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def save(self, commit=True):
        
        orcamento = super().save(commit=False)
        
       
        if orcamento.orca_codi == 0 or orcamento.orca_codi is None:
           
            orcamento.orca_codi = 1 
        
        
        if commit:
            orcamento.save()
        
        return orcamento


class OrcamentoPecasForm(forms.ModelForm):
    class Meta:
        model = OrcamentoPecas
        fields = [
            'peca_orca', 'peca_codi', 'peca_quan', 'peca_unit', 'peca_tota', 'peca_comp'
        ]
        widgets = {
            'peca_orca': forms.Select(attrs={'class': 'form-control'}),
            'peca_codi': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'peca_quan': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peca_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peca_tota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peca_comp': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# Criando um formset inline para OrcamentoPecas
OrcamentoPecasInlineFormSet = inlineformset_factory(
    Orcamento, OrcamentoPecas, form=OrcamentoPecasForm, extra=1, can_delete=True
)