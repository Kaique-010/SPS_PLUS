from django import forms
from .models import Fazenda, Talhao, CategoriaProduto, ProdutoAgro, EstoqueFazenda, MovimentacaoEstoque, AplicacaoInsumos, Animal, EventoAnimal, CicloFlorestal

class FazendaForm(forms.ModelForm):
    class Meta:
        model = Fazenda
        fields = ['nome', 'localizacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome da Fazenda'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Localização'}),
        }

class TalhaoForm(forms.ModelForm):
    class Meta:
        model = Talhao
        fields = ['fazenda', 'nome', 'area', 'unidade_medida']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome do Talhão'}),
            'area': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Área'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Unidade de Medida'}),
        }




class CategoriaProdutoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProduto
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome da Categoria'}),
        }



class ProdutoAgroForm(forms.ModelForm):
    class Meta:
        model = ProdutoAgro
        fields = ['codigo', 'nome', 'categoria', 'unidade_medida', 'descricao', 'custo_medio']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Código'}),
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome do Produto'}),
            'categoria': forms.Select(attrs={'class': 'form-control col-6'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Unidade de Medida'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Descrição'}),
            'custo_medio': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Médio'}),
        }



class EstoqueFazendaForm(forms.ModelForm):
    class Meta:
        model = EstoqueFazenda
        fields = ['fazenda', 'produto', 'quantidade', 'custo_medio_atualizado']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade'}),
            'custo_medio_atualizado': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Médio Atualizado'}),
        }



class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['fazenda', 'produto', 'quantidade', 'tipo', 'usuario', 'documento_referencia', 'motivo', 'custo_unitario']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade'}),
            'tipo': forms.Select(attrs={'class': 'form-control col-6'}),
            'usuario': forms.Select(attrs={'class': 'form-control col-6'}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Documento de Referência'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Motivo'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Unitário'}),
        }



class AplicacaoInsumosForm(forms.ModelForm):
    class Meta:
        model = AplicacaoInsumos
        fields = ['talhao', 'produto', 'quantidade_aplicada', 'responsavel', 'observacoes']
        widgets = {
            'talhao': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade_aplicada': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade Aplicada'}),
            'responsavel': forms.Select(attrs={'class': 'form-control col-6'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
        }



class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['fazenda', 'identificacao', 'raca', 'data_nascimento', 'sexo', 'peso_atual', 'observacoes']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'identificacao': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Identificação'}),
            'raca': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Raça'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Nascimento', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control col-6'}),
            'peso_atual': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Peso Atual'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
        }



class EventoAnimalForm(forms.ModelForm):
    class Meta:
        model = EventoAnimal
        fields = ['animal', 'tipo_evento', 'data_evento', 'custo', 'descricao', 'usuario']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control col-6'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control col-6'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data do Evento'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Descrição'}),
            'usuario': forms.Select(attrs={'class': 'form-control col-6'}),
        }



class CicloFlorestalForm(forms.ModelForm):
    class Meta:
        model = CicloFlorestal
        fields = ['talhao', 'cultura', 'data_plantio', 'data_previsao_colheita', 'data_colheita', 'volume_esperado', 'volume_real', 'custo_total', 'observacoes']
        widgets = {
            'talhao': forms.Select(attrs={'class': 'form-control col-6'}),
            'cultura': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Cultura'}),
            'data_plantio': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Plantio'}),
            'data_previsao_colheita': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data Previsão Colheita'}),
            'data_colheita': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Colheita'}),
            'volume_esperado': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Volume Esperado'}),
            'volume_real': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Volume Real'}),
            'custo_total': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Total'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
        }
