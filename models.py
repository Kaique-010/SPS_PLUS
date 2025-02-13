
from django.db import models


class Saldosprodutos(models.Model):
    sapr_empr = models.IntegerField(primary_key=True)  # The composite primary key (sapr_empr, sapr_fili, sapr_prod) found, that is not supported. The first column is selected.
    sapr_fili = models.IntegerField()
    sapr_prod = models.CharField(max_length=20)
    sapr_sald = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    sapr_said = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)  # Field renamed because it started with '_'.
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)  # Field renamed because it started with '_'.
    prod_codi_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saldosprodutos'
        unique_together = (('sapr_empr', 'sapr_fili', 'sapr_prod'),)
