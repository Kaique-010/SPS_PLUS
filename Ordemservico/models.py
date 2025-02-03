
from django.db import models
from Entidades.models import Entidades


class Ordemservico(models.Model):
    orde_empr = models.IntegerField(primary_key=True) 
    orde_fili = models.IntegerField()
    orde_nume = models.IntegerField(unique=True, blank=True, null=True)  
    orde_data_aber = models.DateField(blank=True, null=True)
    orde_hora_aber = models.TimeField(blank=True, null=True)
    orde_tota = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    orde_enti = models.ForeignKey(Entidades, on_delete=models.CASCADE, related_name='ordens_enti')
    orde_mode = models.CharField(max_length=200, blank=True, null=True)
    orde_care = models.CharField(max_length=200, blank=True, null=True)
    orde_seri = models.CharField(max_length=200, blank=True, null=True)
    orde_aces = models.CharField(max_length=200, blank=True, null=True)
    orde_prev = models.DateField(blank=True, null=True)
    orde_marc = models.IntegerField(blank=True, null=True)
    orde_seto = models.IntegerField(blank=True, null=True)
    orde_tecn = models.ForeignKey(Entidades, on_delete=models.CASCADE, related_name='ordens_tecn')
    orde_gara = models.BooleanField(blank=True, null=True)
    orde_obse = models.TextField(blank=True, null=True)
    orde_stat = models.BooleanField(blank=True, null=True)
    orde_data_fech = models.DateField(blank=True, null=True)
    orde_tipo_serv = models.IntegerField(blank=True, null=True)
    orde_nome_cond = models.CharField(max_length=200, blank=True, null=True)
    orde_plac = models.CharField(max_length=20, blank=True, null=True)
    orde_chas = models.CharField(max_length=200, blank=True, null=True)



    class Meta:
        unique_together = (('orde_empr', 'orde_fili', 'orde_nume'),)
    
    def save(self, *args, **kwargs):
        # Se orde_nume ainda não estiver definido, geramos um novo número sequencial
        if self.orde_nume is None:
            last_order = Ordemservico.objects.order_by('orde_nume').last()
            if last_order:
                self.orde_nume = last_order.orde_nume + 1
            else:
                self.orde_nume = 1  # Começa a contagem a partir de 1 se não houver registros

        super().save(*args, **kwargs)  # Chama o método save da classe pai
