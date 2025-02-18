
from django.db import models
from Entidades.models import Entidades
from produto.models import Produtos

class Orcamento(models.Model):

    pedi_empr = models.IntegerField()
    pedi_fili = models.IntegerField()
    pedi_nume = models.IntegerField(primary_key=True) 
    pedi_data = models.CharField(blank=True, null=True, max_length=255)
    pedi_forn = models.ForeignKey(
        Entidades, on_delete=models.CASCADE, db_column='pedi_forn',
        related_name='orcamentos_por_clientes', null=True, blank=True
    )
    pedi_vend = models.ForeignKey(
        Entidades, on_delete=models.CASCADE, db_column='pedi_vend',
        related_name='orcamentos_como_vendedor', null=True, blank=True
    )
    pedi_cond_rece = models.IntegerField(blank=True, null=True)
    pedi_fret_por = models.CharField(max_length=60, blank=True, null=True)
    pedi_vali = models.CharField(max_length=200, blank=True, null=True)
    pedi_obse = models.TextField(blank=True, null=True)
    pedi_fret = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_veic = models.CharField(max_length=60, blank=True, null=True)
    pedi_plac = models.CharField(max_length=60, blank=True, null=True)
    pedi_desc = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    pedi_tota = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)


    class Statusorcamento(models.TextChoices):
        ABERTO = '1', 'Aberto'
        EM_ANDAMENTO = '2', 'Em Andamento'
        FECHADO = '3', 'Fechado'
        CANCELADO = '4', 'Cancelado'

    pedi_tipo = models.CharField(
        max_length=1, choices=Statusorcamento.choices, blank=True, null=True
    )
    pedi_usua_libe = models.IntegerField(blank=True, null=True)
    pedi_data_libe = models.DateField(blank=True, null=True)
    pedi_hora_libe = models.TimeField(blank=True, null=True)
    pedi_obse_nao_libe = models.TextField(blank=True, null=True)
    pedi_libe = models.BooleanField(blank=True, null=True)
    pedi_nao_libe = models.BooleanField(blank=True, null=True)


    class Meta:
        db_table = 'orcamentosvenda'
        unique_together = (('pedi_empr', 'pedi_fili', 'pedi_nume'),)



class OrcamentoPecas(models.Model):
    peca_id = models.AutoField(primary_key=True)
    peca_empr = models.IntegerField()
    peca_fili = models.IntegerField()
    peca_pedi = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="pecas")
    peca_codi = models.ForeignKey(Produtos,  on_delete=models.CASCADE, related_name="produtos")
    peca_quan = models.DecimalField(max_digits=10, decimal_places=2)
    peca_unit = models.DecimalField(max_digits=10, decimal_places=2)
    peca_tota = models.DecimalField(max_digits=15, decimal_places=2)


    class Meta:
        db_table = 'orcamentotopecas'
    
    
    def save(self, *args, **kwargs):
        self.peca_tota = self.peca_quan * self.peca_unit
        super().save(*args, **kwargs)





class Orcamentosvenda(models.Model):
    pedi_empr = models.IntegerField(primary_key=True) 
    pedi_fili = models.IntegerField()
    pedi_nume = models.IntegerField()
    pedi_forn = models.IntegerField(blank=True, null=True)
    pedi_data = models.DateField(blank=True, null=True)
    pedi_base_ipi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_valo_ipi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_fret = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_segu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_outr = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_desc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_topr = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_base_icms = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_valo_icms = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_outr_icms = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_isen_icms = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_dife_icms = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_outr_ipi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_isen_ipi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_dife_ipi = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_base_icms_st = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_valo_icms_st = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_base_cofin = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_valo_cofin = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_base_pis = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_valo_pis = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_tota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_obse = models.TextField(blank=True, null=True)
    pedi_usua_libe = models.IntegerField(blank=True, null=True)
    pedi_data_libe = models.DateField(blank=True, null=True)
    pedi_hora_libe = models.TimeField(blank=True, null=True)
    pedi_obse_nao_libe = models.TextField(blank=True, null=True)
    pedi_libe = models.BooleanField(blank=True, null=True)
    pedi_nao_libe = models.BooleanField(blank=True, null=True)
    pedi_nume_pedi = models.IntegerField(blank=True, null=True)
    pedi_nume_nota = models.IntegerField(blank=True, null=True)
    pedi_vend = models.IntegerField(blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.
    pedi_cond_rece = models.IntegerField(blank=True, null=True)
    pedi_comp = models.CharField(max_length=60, blank=True, null=True)
    pedi_prae = models.CharField(max_length=60, blank=True, null=True)
    pedi_vali = models.CharField(max_length=60, blank=True, null=True)
    pedi_veic = models.CharField(max_length=60, blank=True, null=True)
    pedi_plac = models.CharField(max_length=60, blank=True, null=True)
    pedi_fret_por = models.CharField(max_length=60, blank=True, null=True)
    pedi_copa = models.CharField(max_length=60, blank=True, null=True)
    pedi_tipo = models.IntegerField(blank=True, null=True)
    pedi_bloq = models.DateField(blank=True, null=True)
    pedi_nume_os = models.IntegerField(blank=True, null=True)
    pedi_repr = models.IntegerField(blank=True, null=True)
    pedi_gere = models.IntegerField(blank=True, null=True)
    pedi_adve = models.IntegerField(blank=True, null=True)
    pedi_cnto = models.CharField(max_length=100, blank=True, null=True)
    pedi_cnto_emai = models.CharField(max_length=100, blank=True, null=True)
    pedi_impo = models.CharField(max_length=60, blank=True, null=True)
    pedi_gara = models.CharField(max_length=60, blank=True, null=True)
    pedi_perc_desc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pedi_fina = models.IntegerField(blank=True, null=True)
    pedi_clon = models.BooleanField(blank=True, null=True)
    pedi_clon_nume = models.IntegerField(blank=True, null=True)
    pedi_clon_usua = models.IntegerField(blank=True, null=True)
    pedi_seto = models.IntegerField(blank=True, null=True)
    pedi_arqu = models.IntegerField(blank=True, null=True)
    pedi_fatu_ppre = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    pedi_fatu_pvol = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    pedi_fatu_pst = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    pedi_fatu_vst = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    pedi_fatu_frac = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orcamentosvenda'
        unique_together = (('pedi_empr', 'pedi_fili', 'pedi_nume'),)