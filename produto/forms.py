from django import forms
from django.forms.models import inlineformset_factory
from produto.models import Produtos, GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca, Tabelaprecos

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = [
            'prod_empr', 'prod_codi', 'prod_nome', 'prod_unme', 'prod_grup', 'prod_sugr',
            'prod_fami', 'prod_loca', 'prod_ncm', 'prod_marc', 'prod_codi_fabr', 'prod_foto'
        ]
        widgets = {
            'prod_codi': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código'
            }),
            'prod_empr': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Empresa'
            }),
            'prod_nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome do Produto'
            }),
            'prod_unme': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Unidade de Medida'
            }),
            'prod_grup': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Grupo'
            }),
            'prod_sugr': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Subgrupo'
            }),
            'prod_fami': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Família'
            }),
            'prod_loca': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Local'
            }),
            'prod_ncm': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'NCM'
            }),
            'prod_marc': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Marca'
            }),
            'prod_codi_fabr': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Código do Fabricante'
            }),
            'prod_foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProdutosForm, self).__init__(*args, **kwargs)
        # Configurando campos opcionais
        self.fields['prod_grup'].required = False
        self.fields['prod_sugr'].required = False  
        self.fields['prod_fami'].required = False
        self.fields['prod_loca'].required = False
        self.fields['prod_marc'].required = False  
        self.fields['prod_foto'].required = False
        self.fields['prod_codi'].required = False

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
            'tabe_marg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': '% a vista'}),
            'tabe_avis': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço a vista'}),
            'tabe_praz': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': 'Preço a Prazo'}),
            'tabe_apra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '% a prazo'}),
            'field_log_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'field_log_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'tabe_hist': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Histórico'}),
            'tabe_cuge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Custo Gerencial'}),
            
        }

TabelaprecosFormSet = inlineformset_factory(Produtos, Tabelaprecos, form=TabelaprecosForm, extra=1)