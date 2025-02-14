# Generated by Django 5.1.1 on 2025-02-14 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Saidas_Produtos', '0001_initial'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saida_produtos',
            name='prod_codi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='produto.produtos'),
        ),
    ]
