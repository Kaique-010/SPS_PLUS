# Generated by Django 5.1.1 on 2025-02-16 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresas',
            fields=[
                ('empr_id', models.AutoField(primary_key=True, serialize=False)),
                ('empr_nome', models.CharField(max_length=100, verbose_name='Nome da Empresa')),
                ('empr_docu', models.CharField(max_length=14, unique=True, verbose_name='CNPJ')),
                ('empr_ie', models.CharField(blank=True, max_length=11, null=True, verbose_name='Inscrição Estadual')),
                ('empr_regi', models.CharField(choices=[('simples_nacional', 'Simples Nacional'), ('regime_normal', 'Regime Normal')], max_length=50, verbose_name='Regime Tributação')),
                ('empr_cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('empr_ende', models.CharField(max_length=100, verbose_name='Endereço')),
                ('empr_nume', models.CharField(max_length=10, verbose_name='Número')),
                ('empr_esta', models.CharField(max_length=2, verbose_name='Estado')),
                ('empr_bair', models.CharField(max_length=100, verbose_name='Bairro')),
                ('empr_cida', models.CharField(max_length=100, verbose_name='Cidade')),
                ('empr_emai', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
            ],
            options={
                'db_table': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='Licencas',
            fields=[
                ('lice_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('lice_docu', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Documento')),
                ('lice_nome', models.CharField(blank=True, max_length=60, null=True, verbose_name='Nome Empresa')),
                ('lice_emai', models.EmailField(blank=True, max_length=150, null=True, verbose_name='E-mail')),
                ('lice_bloq', models.BooleanField(default=False, verbose_name='Ativa?')),
                ('lice_data_cria', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
            ],
            options={
                'verbose_name': 'Licença',
                'db_table': 'licencas',
            },
        ),
        migrations.CreateModel(
            name='Filiais',
            fields=[
                ('fili_id', models.AutoField(primary_key=True, serialize=False)),
                ('fili_nome', models.CharField(max_length=100, verbose_name='Nome da Filial')),
                ('fili_docu', models.CharField(blank=True, max_length=14, null=True, verbose_name='CNPJ')),
                ('fili_ie', models.CharField(blank=True, max_length=11, null=True, verbose_name='Inscrição Estadual')),
                ('fili_regi', models.CharField(choices=[('simples_nacional', 'Simples Nacional'), ('regime_normal', 'Regime Normal')], max_length=50, verbose_name='Regime Tributação')),
                ('fili_cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('fili_ende', models.CharField(max_length=100, verbose_name='Endereço')),
                ('fili_nume', models.CharField(max_length=10, verbose_name='Número')),
                ('fili_esta', models.CharField(max_length=2, verbose_name='Estado')),
                ('fili_bair', models.CharField(max_length=100, verbose_name='Bairro')),
                ('fili_cida', models.CharField(max_length=100, verbose_name='Cidade')),
                ('fili_emai', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filiais', to='licencas.empresas')),
            ],
            options={
                'db_table': 'filiais',
                'unique_together': {('empresa', 'fili_docu')},
            },
        ),
        migrations.AddField(
            model_name='empresas',
            name='licenca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to='licencas.licencas'),
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('login', models.CharField(max_length=50, unique=True, verbose_name='Login')),
                ('data_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, null=True)),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='E-mail')),
                ('telefone', models.CharField(blank=True, max_length=14, null=True, verbose_name='Telefone')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('empresas', models.ManyToManyField(related_name='usuarios', to='licencas.empresas')),
                ('filiais', models.ManyToManyField(related_name='usuarios', to='licencas.filiais')),
                ('licenca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='licencas.licencas')),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.AlterUniqueTogether(
            name='empresas',
            unique_together={('licenca', 'empr_docu')},
        ),
    ]
