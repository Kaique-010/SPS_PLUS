from django.db import models
from Entidades.models import Entidades
from licencas.models import Usuarios
from produto.models import Produtos

    

class SaidasEstoque(models.Model):
    id = None
    said_sequ = models.IntegerField()
    said_empr = models.CharField(max_length=100)
    said_fili = models.CharField(max_length=100)
    said_prod = models.ForeignKey(Produtos, on_delete=models.PROTECT, blank=False, null=False, related_name='saidas_produtos', db_column='said_prod', primary_key=True)
    said_enti = models.ForeignKey(Entidades, on_delete=models.PROTECT, blank=False, null=False, related_name='saidas', db_column='said_enti')
    said_data = models.DateField()
    said_quan = models.DecimalField(max_digits=10, decimal_places=2)
    said_tota = models.DecimalField(max_digits=10, decimal_places=2)
    said_obse = models.CharField('Observações', max_length=100, blank=True, null=True)
    said_usua = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='said_usua')

    class Meta:
        db_table = 'saidasestoque'
        ordering = ['-said_data']
        verbose_name = 'Saída Estoque'
        verbose_name_plural = 'Saídas Estoque'
        constraints = [
            models.UniqueConstraint(fields=['said_empr', 'said_fili', 'said_prod', 'said_data'], name='pk_saida_estoque')
        ]

    def __str__(self):
        return f'Saída {self.said_prod} - {self.said_data}'
