# Generated by Django 5.1.1 on 2025-02-17 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Entidades', '0001_initial'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaidasEstoque',
            fields=[
                ('said_empr', models.CharField(max_length=100)),
                ('said_fili', models.CharField(max_length=100)),
                ('said_prod', models.ForeignKey(db_column='said_prod', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='saidas_produtos', serialize=False, to='produto.produtos')),
                ('said_data', models.DateField()),
                ('said_quan', models.DecimalField(decimal_places=2, max_digits=10)),
                ('said_tota', models.DecimalField(decimal_places=2, max_digits=10)),
                ('said_obse', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observações')),
                ('said_enti', models.ForeignKey(db_column='said_enti', on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='Entidades.entidades')),
            ],
            options={
                'verbose_name': 'Saída Estoque',
                'verbose_name_plural': 'Saídas Estoque',
                'db_table': 'saidasestoque',
                'ordering': ['-said_data'],
                'constraints': [models.UniqueConstraint(fields=('said_empr', 'said_fili', 'said_prod', 'said_data'), name='pk_saida_estoque')],
            },
        ),
    ]
