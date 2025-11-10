# models.py
from django.db import models

class Orcamentos(models.Model):
    pedi_empr = models.IntegerField()
    pedi_fili = models.IntegerField()
    pedi_nume = models.IntegerField(primary_key=True, unique=True, db_column='pedi_nume')
    pedi_forn = models.CharField(db_column='pedi_forn',max_length=60)
    pedi_data = models.DateField()
    pedi_topr = models.DecimalField(db_column='pedi_topr', max_digits=15, decimal_places=2,blank=True, null=True)
    pedi_tota = models.DecimalField(decimal_places=2, max_digits=15)
    pedi_vend = models.CharField( db_column='pedi_vend', max_length=15,blank=True, null=True)  
    pedi_obse = models.TextField(blank=True, null=True)
    pedi_nume_pedi = models.IntegerField(db_column='pedi_nume_pedi',blank=True, null=True)
    pedi_desc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
 


    class Meta:
        db_table = 'orcamentosvenda'
        managed = False

    def __str__(self):
        return f"Pedido {self.pedi_nume} - {self.pedi_forn}"

    
    
class ItensOrcamento(models.Model):
    iped_empr = models.IntegerField(db_column='iped_empr')
    iped_fili = models.IntegerField()
    iped_pedi = models.ForeignKey(
        Orcamentos,
        to_field='pedi_nume',
        db_column='iped_pedi',
        on_delete=models.DO_NOTHING,
        related_name='itens',
        primary_key=True,
        db_constraint=False,
    )
    iped_item = models.IntegerField()
    iped_prod = models.CharField(max_length=60, db_column='iped_prod') 
    iped_quan = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    iped_suto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    iped_unit = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    iped_tota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    iped_desc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    iped_unli = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    iped_forn = models.IntegerField(blank=True, null=True)
    iped_pdes_item = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    iped_data = models.DateField()


    class Meta:
        db_table = 'itensorcamentovenda'
        unique_together = (('iped_empr', 'iped_fili', 'iped_pedi', 'iped_item'),)
        managed = False

