# Generated by Django 5.1.1 on 2025-01-30 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Saidas_Produtos', '0002_rename_produto_saida_produtos_produto_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='saida_produtos',
            name='data',
            field=models.DateField(blank=True, null=True, verbose_name='Data Saída'),
        ),
    ]
