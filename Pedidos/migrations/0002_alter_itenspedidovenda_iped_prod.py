# Generated by Django 5.1.1 on 2025-02-19 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0001_initial'),
        ('produto', '0002_alter_saldoproduto_sapr_empr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itenspedidovenda',
            name='iped_prod',
            field=models.ForeignKey(db_column='prod_codi', default=1, on_delete=django.db.models.deletion.CASCADE, to='produto.produtos'),
            preserve_default=False,
        ),
    ]
