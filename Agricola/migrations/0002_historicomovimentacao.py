# Generated by Django 5.1.1 on 2025-02-20 01:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agricola', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoMovimentacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=10)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('fazenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agricola.fazenda')),
                ('movimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico', to='Agricola.movimentacaoestoque')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agricola.produtoagro')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'historico_movimentacoes',
            },
        ),
    ]
