from django import forms
from Entidades.models import Entidades
from produto.models import Produtos
from .models import Orcamento, OrcamentoPecas
from django.forms import inlineformset_factory
from django.db.models import Max


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            'pedi_empr', 'pedi_fili', 'pedi_nume', 'pedi_data', 'pedi_forn',
            'pedi_vend', 'pedi_fret_por', 'pedi_obse', 'pedi_vali',
            'pedi_desc', 'pedi_tota', 'pedi_tipo', 'pedi_fret'
        ]
        widgets = {
            'pedi_empr': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'pedi_fili': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Filial'}),
            'pedi_nume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Código do orçamento'}),
            'pedi_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pedi_forn': forms.HiddenInput(),
            'pedi_vend': forms.HiddenInput(),
            'pedi_fret_por': forms.NumberInput(attrs={'class': 'form-control'}),
            'pedi_fret': forms.NumberInput(attrs={'class': 'form-control'}),
            'pedi_vali': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pedi_obse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pedi_desc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pedi_tota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pedi_forn'].queryset = Entidades.objects.filter(enti_tipo_enti__in=['CL', 'AM'])  # Clientes e Ambos
        self.fields['pedi_vend'].queryset = Entidades.objects.filter(enti_tipo_enti__in=['VE', 'AM'])  # Vendedores e Ambos

    def save(self, commit=True):
        orcamento = super().save(commit=False)

        if orcamento.pedi_nume is None or orcamento.pedi_nume == 0:
            max_nume = Orcamento.objects.aggregate(max_nume=Max('pedi_nume'))['max_nume'] or 0
            orcamento.pedi_nume = max_nume + 1

        if commit:
            orcamento.save()

        return orcamento


class OrcamentoPecasForm(forms.ModelForm):
    class Meta:
        model = OrcamentoPecas  # Corrigido, sem parênteses
        fields = ['peca_pedi', 'peca_codi', 'peca_quan', 'peca_unit', 'peca_tota']
        widgets = {
            'peca_pedi': forms.Select(attrs={'class': 'form-control'}),
            'peca_codi': forms.Select(attrs={'class': 'form-control'}),
            'peca_quan': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peca_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peca_tota': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        }

    def clean_peca_quan(self):
        quantidade = self.cleaned_data.get('peca_quan')
        if quantidade is not None and quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade

    def clean_peca_unit(self):
        preco_unitario = self.cleaned_data.get('peca_unit')
        if preco_unitario is not None and preco_unitario <= 0:
            raise forms.ValidationError("O preço unitário deve ser maior que zero.")
        return preco_unitario


OrcamentoPecasInlineFormSet = inlineformset_factory(
    Orcamento,
    OrcamentoPecas,
    form=OrcamentoPecasForm,
    extra=1,
    can_delete=True
)
