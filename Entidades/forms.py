from django import forms
from django.db import transaction
from django.db.models import Max
from .models import Entidades
import logging

logger = logging.getLogger(__name__)


class EntidadesForm(forms.ModelForm):
    class Meta:
        model = Entidades
        fields = [
            'enti_empr', 'enti_clie', 'enti_nome', 'enti_tipo_enti', 'enti_fant', 
            'enti_cpf', 'enti_cnpj', 'enti_insc_esta', 'enti_cep', 'enti_ende', 
            'enti_nume', 'enti_cida', 'enti_esta', 'enti_fone', 'enti_celu', 
            'enti_emai', 'enti_emai_empr'
        ]
        widgets = {
            'enti_empr': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'enti_clie': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cliente'}),
            'enti_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'enti_tipo_enti': forms.Select(attrs={'class': 'form-control'}),
            'enti_fant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Fantasia'}),
            'enti_cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF', 'maxlength': '11'}),
            'enti_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'maxlength': '14'}),
            'enti_insc_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'enti_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '8'}),
            'enti_ende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'enti_nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'enti_cida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'enti_esta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'maxlength': '2'}),
            'enti_fone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'maxlength': '14'}),
            'enti_celu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'maxlength': '15'}),
            'enti_emai': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Pessoal'}),
            'enti_emai_empr': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email da Empresa'}),
        }

    def __init__(self, *args, db_name=None, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_name = db_name  # Guarda o nome do banco para ser usado no save()
        self.request = request  # Store the request object

        # Tornar certos campos não obrigatórios
        for field in ['enti_cpf', 'enti_cnpj', 'enti_fone', 'enti_emai', 'enti_emai_empr',
                    'enti_insc_esta', 'enti_empr', 'enti_fant', 'enti_ende', 
                    'enti_cida', 'enti_esta', 'enti_clie']:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('enti_cpf')
        cnpj = cleaned_data.get('enti_cnpj')
        ie = cleaned_data.get('enti_insc_esta')

        # Validação para não permitir CPF junto com CNPJ ou Inscrição Estadual
        if cpf and (cnpj or ie):
            raise forms.ValidationError("Se o CPF for fornecido, CNPJ e Inscrição Estadual não devem ser preenchidos.")
        
        return cleaned_data

    def save(self, commit=True):
        logger.debug("Método save() chamado.")  # Log de depuração
        if not hasattr(self, 'request') or not self.request:
            raise ValueError("Erro: requisição não definida no formulário. Verifique se o request foi passado corretamente.")

        db_alias = self.request.db_alias
        if not db_alias:
            raise ValueError("Erro: banco de dados não definido no formulário. Verifique se a sessão contém 'banco'.")

        instance = super().save(commit=False)

        if instance.enti_empr is None:
            raise ValueError("A empresa (`enti_empr`) deve ser informada antes de salvar.")

        with transaction.atomic(using=db_alias):
            # Verifica se é uma criação (instance.pk é None) ou uma edição (instance.pk não é None)
            if not instance.enti_clie:
                # Somente para criação: calcula o próximo enti_clie
                logger.debug(f"Banco de dados sendo usado: {db_alias}")
                logger.debug(f"Consulta SQL: SELECT MAX(enti_clie) FROM Entidades;")

                # Obtém o maior valor de `enti_clie` no banco de dados
                ultimo_codigo = Entidades.objects.using(db_alias).aggregate(Max("enti_clie"))["enti_clie__max"]
                
                # Log para depuração
                logger.debug(f"Último código encontrado: {ultimo_codigo}")

                # Se não houver registros, define como 1, caso contrário, incrementa o último código
                if ultimo_codigo is None:
                    instance.enti_clie = 1
                else:
                    instance.enti_clie = ultimo_codigo + 1

                # Log para depuração
                logger.debug(f"Novo código definido: {instance.enti_clie}")
            else:
                # Para edição, mantém o enti_clie existente
                logger.debug(f"Editando registro existente. enti_clie mantido: {instance.enti_clie}")

            if commit:
                instance.save(using=db_alias)
                logger.debug(f"Registro salvo com sucesso: {instance.enti_clie}")

        return instance