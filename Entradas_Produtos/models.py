from django.db import models
from Entidades.models import Entidades
from licencas.models import Usuarios
from produto.models import Produtos

    

class EntradaEstoque(models.Model):
    id = None
    entr_sequ = models.IntegerField()
    entr_empr = models.CharField(max_length=100)
    entr_fili = models.CharField(max_length=100)
    entr_prod = models.ForeignKey(Produtos, on_delete=models.PROTECT, blank=False, null=False, related_name='entradas_produtos', db_column='entr_prod', primary_key=True)
    entr_enti = models.ForeignKey(Entidades, on_delete=models.PROTECT, blank=False, null=False, related_name='entradas', db_column='entr_enti')
    entr_data = models.DateField()
    entr_quan = models.DecimalField(max_digits=10, decimal_places=2)
    entr_tota = models.DecimalField(max_digits=10, decimal_places=2)
    entr_obse = models.CharField('Observações', max_length=100, blank=True, null=True)
    entr_usua = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='entr_usua')

    class Meta:
        db_table = 'entradasestoque'
        ordering = ['entr_sequ']
        verbose_name = 'Entrada Estoque'
        verbose_name_plural = 'Entradas Estoque'
        unique_together = (('entr_empr', 'entr_fili', 'entr_prod', 'entr_data'),)  # 🔥 Chave composta

    def __str__(self):
        return f'Entrada {self.entr_prod} - {self.entr_data}'
