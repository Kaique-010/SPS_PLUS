from django import forms
from django.forms.models import inlineformset_factory
from produto.models import Produtos, GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca, Tabelaprecos

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = [
            'prod_empr','produto_codigo', 'nome_produto', 'unidade_medida', 'grupo', 'subgrupo',
            'familia', 'local', 'ncm', 'marca', 'codigo_fabricante', 'foto'
        ]
        widgets = {
            'produto_codigo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'prod_empr':forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Empresa'
            }),
            'nome_produto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome do Produto'
            }),
            'unidade_medida': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Unidade de Medida'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Grupo'
            }),
            'subgrupo': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Subgrupo'
            }),
            'familia': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Família'
            }),
            'local': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Local'
            }),
            'ncm': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'NCM'
            }),
            'marca': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Marca'
            }),
            'codigo_fabricante': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código do Fabricante'
            }),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            }
    
    def __init__(self, *args, **kwargs):
        super(ProdutosForm, self).__init__(*args, **kwargs)
        # Configurando campos opcionais
        self.fields['grupo'].required = False
        self.fields['subgrupo'].required = False  
        self.fields['familia'].required = False
        self.fields['local'].required = False
        self.fields['marca'].required = False  
        self.fields['foto'].required = False
        self.fields['produto_codigo'].required = False

class GrupoForm(forms.ModelForm):
   class Meta:
       model = GrupoProduto
       fields = '__all__'
       widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Descrição'
            }),
            }
       

class SubgrupoForm(forms.ModelForm):
   class Meta:
       model = SubgrupoProduto
       fields = '__all__'
       widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Descrição'
            }),
            }


class FamiliaForm(forms.ModelForm):
    class Meta:
        model= FamiliaProduto
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Descrição'
            }),
            }
        
class MarcaForm(forms.ModelForm):
   class Meta:
       model = Marca
       fields = '__all__'
       widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome'
            }),
            }
    


class TabelaprecosForm(forms.ModelForm):
    class Meta:
        model = Tabelaprecos
        fields = [
            'tabe_fili', 'tabe_prco', 'tabe_icms', 'tabe_desc', 'tabe_vipi', 'tabe_pipi', 'tabe_fret', 
            'tabe_desp', 'tabe_cust', 'tabe_marg', 'tabe_impo', 'tabe_avis', 'tabe_praz', 'tabe_apra', 
            'tabe_vare', 'field_log_data', 'field_log_time', 'tabe_valo_st', 'tabe_perc_reaj', 'tabe_hist',
            'tabe_cuge', 'tabe_entr', 'tabe_perc_st'
        ]

        widgets = {
            'tabe_prco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço de Compra'}),
            'tabe_fret': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': '% Frete'}),
            'tabe_desp': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': 'Despesas'}),
            'tabe_cust': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Custo Gerencial'}),
            'tabe_marg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': '% a vista'}),
            'tabe_avis': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço a vista'}),
            'tabe_praz': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': 'Preço a Prazo'}),
            'tabe_apra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '% a prazo'}),
            'field_log_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'field_log_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'tabe_perc_reaj': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Reajuste'}),
            'tabe_hist': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Histórico'}),
            'tabe_cuge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Custo Geral'}),
            'tabe_entr': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

TabelaprecosFormSet = inlineformset_factory(Produtos, Tabelaprecos, form=TabelaprecosForm, extra=1)