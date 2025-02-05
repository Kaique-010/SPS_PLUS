# Generated by Django 5.1.5 on 2025-02-05 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Entidades', '0002_alter_entidades_enti_fant_alter_entidades_enti_nome'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saida_Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Data de Modificação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data Saída')),
                ('quantidade', models.IntegerField()),
                ('documento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Nº Documento')),
                ('observacoes', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observações')),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='Entidades.entidades')),
                ('produto_codigo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='produto.produtos')),
            ],
            options={
                'verbose_name': 'Saída Produto',
                'verbose_name_plural': 'Saída Produtos',
            },
        ),
    ]
