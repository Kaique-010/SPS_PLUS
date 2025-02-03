
from django.db import models
from Entidades.models import Entidades
from produto.models import Produtos



class Orcamento(models.Model):
    orca_id = models.AutoField(primary_key=True)
    orca_empr = models.IntegerField()
    orca_fili = models.IntegerField()
    orca_codi = models.IntegerField()
    orca_aber = models.CharField(blank=True, null=True)
    orca_enti = models.ForeignKey(Entidades, on_delete=models.CASCADE, db_column='orca_enti', related_name='orcamentos_por_clientes', null=True, blank=True)
    orca_vend = models.ForeignKey(Entidades, on_delete=models.CASCADE, db_column='orca_vend', related_name='orcamentos_como_vendedor', null=True, blank=True)
    orca_cond = models.IntegerField(blank=True, null=True)
    orca_resp = models.IntegerField(blank=True, null=True)
    orca_tipo_fret = models.IntegerField(blank=True, null=True)
    orca_vali = models.CharField(max_length=200, blank=True, null=True)
    orca_tipo_impo = models.CharField(max_length=200, blank=True, null=True)
    orca_praz_entr = models.CharField(max_length=200, blank=True, null=True)
    orca_obse = models.TextField(blank=True, null=True)
    orca_valo_fret = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    orca_valo_outr = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    orca_valo_desc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    orca_valo_tota = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    orca_orde_refe = models.IntegerField(blank=True, null=True)
    orca_gara = models.CharField(max_length=200, blank=True, null=True)
    orca_data_alte = models.DateField(blank=True, null=True)
    orca_stat = models.BooleanField(blank=True, null=True)
    orca_soli = models.CharField(max_length=200, blank=True, null=True)
    orca_refe = models.CharField(max_length=50, blank=True, null=True)
    orca_data_repr = models.DateField(blank=True, null=True)
    orca_data_apro = models.DateField(blank=True, null=True)
    orca_bloq = models.DateField(blank=True, null=True)
    orca_tipo_gara = models.BooleanField(blank=True, null=True)
    orca_tipo_cort = models.BooleanField(blank=True, null=True)
    orca_tipo_seco = models.BooleanField(blank=True, null=True)

    class Meta:

        db_table = 'orcamento'
        unique_together = (('orca_empr', 'orca_fili', 'orca_codi'),)


class OrcamentoPecas(models.Model):
    peca_id = models.AutoField(primary_key=True)
    peca_empr = models.IntegerField()
    peca_fili = models.IntegerField()
    peca_orca = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="pecas")
    peca_codi = models.ForeignKey(Produtos,  on_delete=models.CASCADE, related_name="produtos")
    peca_quan = models.DecimalField(max_digits=10, decimal_places=2)
    peca_unit = models.DecimalField(max_digits=10, decimal_places=2)
    peca_tota = models.DecimalField(max_digits=15, decimal_places=2)
    peca_comp = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'orcamentopecas'