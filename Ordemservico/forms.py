from django import forms
from Ordemservico.models import Ordemservico

class OrdemservicoForm(forms.ModelForm):
    class Meta:
        model = Ordemservico
        fields = '__all__'  
        widgets = {
            'orde_empr': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_fili': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_nume': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_data_aber': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orde_hora_aber': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'orde_tota': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_enti': forms.Select(attrs={'class': 'form-control'}),
            'orde_mode': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_care': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_seri': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_aces': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_prev': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orde_marc': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_seto': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_tecn': forms.Select(attrs={'class': 'form-control'}),
            'orde_gara': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'orde_obse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'orde_stat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'orde_data_fech': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orde_tipo_serv': forms.NumberInput(attrs={'class': 'form-control'}),
            'orde_nome_cond': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_plac': forms.TextInput(attrs={'class': 'form-control'}),
            'orde_chas': forms.TextInput(attrs={'class': 'form-control'}),
            # Adicione outros campos conforme necessário...
        }

