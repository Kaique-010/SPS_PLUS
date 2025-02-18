# Generated by Django 5.1.1 on 2025-02-18 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licencas', '0001_initial'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saldoproduto',
            name='sapr_empr',
            field=models.ForeignKey(db_column='sapr_empr', on_delete=django.db.models.deletion.CASCADE, to='licencas.empresas'),
        ),
        migrations.AlterField(
            model_name='saldoproduto',
            name='sapr_fili',
            field=models.ForeignKey(db_column='sapr_fili', on_delete=django.db.models.deletion.CASCADE, to='licencas.filiais'),
        ),
        migrations.AlterField(
            model_name='saldoproduto',
            name='sapr_sald',
            field=models.DecimalField(blank=True, db_column='sapr_sald', decimal_places=4, max_digits=15, null=True),
        ),
    ]
