from django import forms
from produto.models import Produtos, GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca

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
    