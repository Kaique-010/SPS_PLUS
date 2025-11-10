from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Licencas(models.Model):
    lice_id = models.AutoField('Id', primary_key=True)
    lice_docu = models.CharField('Documento', max_length=60, unique=True, blank=True, null=True)
    lice_nome = models.CharField('Nome Empresa', max_length=60, blank=True, null=True)
    lice_emai = models.EmailField('E-mail', max_length=150, blank=True, null=True)
    lice_bloq = models.BooleanField('Ativa?', default=False)
    lice_data_cria = models.DateField('Data de Criação', auto_now_add=True)
    db_config = models.TextField('Configuração do Banco de Dados')

    class Meta:
        db_table = 'licencas'
        verbose_name = 'Licença'

    def __str__(self):
        return f"Licença {self.lice_id} - {self.lice_docu} - {self.lice_nome}"


class Licencas2013(models.Model):
    """
    Modelo somente leitura para a tabela existente 'licencas2013' no banco principal.
    Usado para obter o mapeamento de slug -> banco (campo 'lice_banc').
    """
    lice_docu = models.CharField('Documento', max_length=60, primary_key=True)
    lice_nome = models.CharField('Nome Empresa', max_length=120, blank=True, null=True)
    lice_banc = models.CharField('Banco', max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'licencas2013'
        managed = False

    def slug(self):
        nome = (self.lice_nome or '').strip().lower()
        return nome.replace(' ', '').replace('-', '')


class Empresas(models.Model):
    empr_codi = models.AutoField(primary_key=True, db_column='empr_codi')
    empr_nome = models.CharField('Nome da Empresa', max_length=100)
    empr_docu = models.CharField('CNPJ', max_length=14, unique=True, db_column='empr_cnpj')
    empr_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True, db_column='empr_insc_esta')
    empr_regi = models.CharField('Regime Tributação', max_length=50, choices=[
        ('simples_nacional', 'Simples Nacional'),
        ('regime_normal', 'Regime Normal')
    ])
    empr_cep = models.CharField('CEP', max_length=8, )
    empr_ende = models.CharField('Endereço', max_length=100)
    empr_nume = models.CharField('Número', max_length=10)
    empr_esta = models.CharField('Estado', max_length=2)
    empr_bair = models.CharField('Bairro', max_length=100)
    empr_cida = models.CharField('Cidade', max_length=100)
    empr_emai = models.EmailField('E-mail', blank=True, null=True)

    class Meta:
        db_table = 'empresas'
        
    
    def __str__(self):
        return self.empr_nome



class Filiais(models.Model):
    empr_codi = models.OneToOneField(Empresas, primary_key=True, db_column='empr_codi', on_delete=models.CASCADE)
    empr_nome = models.CharField('Nome da Empresa', max_length=100)
    empr_docu = models.CharField('CNPJ', max_length=14, unique=True, db_column='empr_cnpj')
    empr_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True, db_column='empr_insc_esta')
    empr_regi = models.CharField('Regime Tributação', max_length=50, choices=[
        ('simples_nacional', 'Simples Nacional'),
        ('regime_normal', 'Regime Normal')
    ])
    empr_cep = models.CharField('CEP', max_length=8, )
    empr_ende = models.CharField('Endereço', max_length=100)
    empr_nume = models.CharField('Número', max_length=10)
    empr_esta = models.CharField('Estado', max_length=2)
    empr_bair = models.CharField('Bairro', max_length=100)
    empr_cida = models.CharField('Cidade', max_length=100)
    empr_emai = models.EmailField('E-mail', blank=True, null=True)

    class Meta:
        db_table = 'filiais'
    
    def __str__(self):
        return self.empr_nome


class UsuarioManager(BaseUserManager):
    def create_user(self, login, nome, email, password=None, **extra_fields):
        """
        Cria e retorna um usuário com login, nome, email e senha.
        """
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(login=login, nome=nome, email=email, **extra_fields)
        # Atende ao legado: armazena senha em texto puro na coluna usua_senh_mobi
        user.password = password or ''
        user.save(using=self._db)
        return user

    def create_superuser(self, login, nome, email, password=None, licenca=None, **extra_fields):
        """
        Cria e retorna um superusuário com login, nome, email e senha.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('O email deve ser fornecido')

        if licenca:
            extra_fields.setdefault('licenca', licenca)
        else:
            raise ValueError('Licença deve ser fornecida ao criar superusuário.')

        # Garantir que 'licenca' seja um campo obrigatório no modelo de usuários
        if 'licenca' not in extra_fields:
            raise ValueError("Licença é obrigatória para criar superusuário.")
        
        return self.create_user(login, nome, email, password, **extra_fields)




class Usuarios(AbstractBaseUser):
    usua_codi = models.AutoField("ID", primary_key=True)
    nome = models.CharField("Nome", max_length=100, db_column='usua_nome', unique=True)
    password = models.CharField(max_length=128, db_column='usua_senh_mobi', blank=True, null=True)
    # Usar a coluna correta 'last_login' (timestamp) criada via migração
    last_login = None
 

    empresas = models.ManyToManyField(Empresas, related_name="usuarios")
    filiais = models.ManyToManyField(Filiais, related_name="usuarios")


    objects = UsuarioManager()
    USERNAME_FIELD = "nome"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return self.nome

    @property
    def usua_senh_mobi(self):
        """Obtém o valor do campo legado 'usua_senh_mobi' diretamente do banco.
        Não requer migrações e assume que a coluna existe na tabela.
        """
        from django.db import connections
        # Usa o alias da instância, definido pelo ORM
        db_alias = getattr(self._state, 'db', 'default') or 'default'
        try:
            with connections[db_alias].cursor() as cursor:
                cursor.execute("SELECT usua_senh_mobi FROM usuarios WHERE usua_codi = %s", [self.pk])
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception:
            return None