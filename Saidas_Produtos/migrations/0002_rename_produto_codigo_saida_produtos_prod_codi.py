# Generated by Django 5.1.5 on 2025-02-10 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Saidas_Produtos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saida_produtos',
            old_name='produto_codigo',
            new_name='prod_codi',
        ),
    ]
