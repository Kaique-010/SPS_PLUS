import os
from licencas.models import Licencas2013


def carregar_licencas_dict():
    """Retorna uma lista de dicts com slug e dados de conexão.
    Fonte: tabela 'licencas2013' no banco padrão (save1).
    """
    host = os.getenv("DB_HOST", "base.rtalmeida.com.br")
    port = os.getenv("DB_PORT", "5432")

    data = []
    # Usa o banco padrão para ler licencas2013
    for lic in Licencas2013.objects.using('default').all():
        slug = lic.slug()
        db_name = lic.lice_banc or slug  # preferir campo banco
        # Normaliza documento para bater com o que o backend usa
        raw_doc = lic.lice_docu or ""
        norm_doc = str(raw_doc).replace(".", "").replace("-", "").replace("/", "").strip()
        data.append({
            "slug": slug,
            "cnpj": norm_doc,
            "db_name": db_name,
            "db_host": host,
            "db_port": port,
        })

    return data