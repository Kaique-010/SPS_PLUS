from django.db import models

class Licencas(models.Model):
    lice_id = models.AutoField('Id', primary_key=True)
    lice_docu = models.CharField('Documento', max_length=60, blank=True, null=True)
    lice_nome = models.CharField('Nome Empresa', max_length=60, blank=True, null=True)
    lice_emai = models.EmailField('E-mail', max_length=150, blank=True, null=True)
    lice_bloq = models.BooleanField('Ativa?', default=False)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    class Meta:
        db_table = 'licencas'

    def __str__(self):
        return f"Licença {self.lice_id} - {self.lice_docu}"


class Usuarios(models.Model):
    usua_codi = models.AutoField('ID', primary_key=True)
    usua_nome = models.CharField('Nome', max_length=30, blank=True, null=True)
    usua_login = models.CharField('Login', max_length=30, blank=True, null=True)
    usua_data_nasc = models.DateField('Data Nascimento', blank=True, null=True)
    usua_sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, null=True)
    usua_emai = models.EmailField('E-mail', max_length=100, blank=True, null=True)
    usua_fone = models.CharField('Telefone', max_length=14, blank=True, null=True)
    usua_senh = models.CharField('Senha', max_length=128)
    usua_bloq = models.BooleanField('Ativo?', default=True)
    usua_libe_clie_bloq = models.BooleanField('Liberação Cliente Bloqueado', default=False)
    usua_libe_pedi_comp = models.BooleanField('Liberação Pedido Comprado', default=False)
    licenca = models.ForeignKey(Licencas, on_delete=models.CASCADE, related_name='usuarios', blank=True, null=True)
    field_log_data = models.DateField(db_column='_log_data', blank=True, null=True)
    field_log_time = models.TimeField(db_column='_log_time', blank=True, null=True)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.usua_nome or f"Usuário {self.usua_codi}"


class Empresas(models.Model):
    empr_id = models.AutoField('ID', primary_key=True)
    empr_nome = models.CharField('Nome da Empresa', max_length=100)
    empr_docu = models.CharField('Documento', max_length=14, blank=True, null=True)
    empr_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True)
    empr_regi = models.CharField('Regime Tributação', max_length=50, choices=[('simples_nacional','Simples Nacional'), ('regime_normal', 'Regime Normal')])
    empr_cep = models.CharField('CEP',max_length=8)
    empr_ende = models.CharField('Endereço', max_length=100)
    empr_nume = models.CharField('Numero', max_length=10)
    empr_esta = models.CharField('Estado', max_length=2)
    empr_bair = models.CharField('Bairro', max_length=100)
    empr_cida = models.CharField('cidade', max_length=100)
    empr_emai = models.EmailField('E-mail', blank=True, null=True)
    licenca = models.ForeignKey(Licencas, on_delete=models.CASCADE, related_name='empresas')
   

    class Meta:
        db_table = 'empresas'

    def __str__(self):
        return self.empr_nome


class Filiais(models.Model):
    fili_id = models.AutoField('ID', primary_key=True)
    fili_nome = models.CharField('Nome da Filial', max_length=100)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='filiais')
    fili_docu = models.CharField('Documento', max_length=14, blank=True, null=True)
    fili_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True)
    fili_regi = models.CharField('Regime Tributação', max_length=50, choices=[('simples_nacional','Simples Nacional'), ('regime_normal', 'Regime Normal')])
    fili_cep = models.CharField('CEP',max_length=8)
    fili_ende = models.CharField('Endereço', max_length=100)
    fili_nume = models.CharField('Numero', max_length=10)
    fili_esta = models.CharField('Estado', max_length=2)
    fili_bair = models.CharField('Bairro', max_length=100)
    fili_cida = models.CharField('cidade', max_length=100)
    fili_emai = models.EmailField('E-mail', blank=True, null=True)

    class Meta:
        db_table = 'filiais'

    def __str__(self):
        return self.fili_nome
