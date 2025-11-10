from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                # Modelo de estado para Empresas (não gerenciado, tabela já existe)
                migrations.CreateModel(
                    name="Empresas",
                    fields=[
                        ("empr_codi", models.AutoField(primary_key=True, serialize=False)),
                        ("empr_nome", models.CharField(max_length=100)),
                    ],
                    options={
                        "db_table": "empresas",
                        "managed": False,
                    },
                ),
                # Modelo de estado para Filiais (não gerenciado, tabela já existe)
                migrations.CreateModel(
                    name="Filiais",
                    fields=[
                        (
                            "empr_codi",
                            models.OneToOneField(
                                primary_key=True,
                                serialize=False,
                                to="licencas.Empresas",
                                on_delete=django.db.models.deletion.CASCADE,
                                db_column="empr_codi",
                            ),
                        ),
                        ("empr_nome", models.CharField(max_length=100)),
                    ],
                    options={
                        "db_table": "filiais",
                        "managed": False,
                    },
                ),
                # Modelo de estado para Usuarios (não gerenciado, tabela já existe)
                migrations.CreateModel(
                    name="Usuarios",
                    fields=[
                        ("usua_codi", models.AutoField(primary_key=True, serialize=False)),
                        ("nome", models.CharField(max_length=100, unique=True)),
                        ("password", models.CharField(max_length=128, blank=True, null=True)),
                    ],
                    options={
                        "db_table": "usuarios",
                        "managed": False,
                    },
                ),
            ],
        )
    ]