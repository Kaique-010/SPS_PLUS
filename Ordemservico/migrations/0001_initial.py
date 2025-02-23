# Generated by Django 5.1.1 on 2025-02-23 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Entidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordemservico',
            fields=[
                ('orde_empr', models.IntegerField(primary_key=True, serialize=False)),
                ('orde_fili', models.IntegerField()),
                ('orde_nume', models.IntegerField(blank=True, null=True, unique=True)),
                ('orde_data_aber', models.DateField(blank=True, null=True)),
                ('orde_hora_aber', models.TimeField(blank=True, null=True)),
                ('orde_tota', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('orde_mode', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_care', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_seri', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_aces', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_prev', models.DateField(blank=True, null=True)),
                ('orde_marc', models.IntegerField(blank=True, null=True)),
                ('orde_seto', models.IntegerField(blank=True, null=True)),
                ('orde_gara', models.BooleanField(blank=True, null=True)),
                ('orde_obse', models.TextField(blank=True, null=True)),
                ('orde_stat', models.BooleanField(blank=True, null=True)),
                ('orde_data_fech', models.DateField(blank=True, null=True)),
                ('orde_tipo_serv', models.IntegerField(blank=True, null=True)),
                ('orde_nome_cond', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_plac', models.CharField(blank=True, max_length=20, null=True)),
                ('orde_chas', models.CharField(blank=True, max_length=200, null=True)),
                ('orde_enti', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens_enti', to='Entidades.entidades')),
                ('orde_tecn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens_tecn', to='Entidades.entidades')),
            ],
            options={
                'unique_together': {('orde_empr', 'orde_fili', 'orde_nume')},
            },
        ),
    ]
