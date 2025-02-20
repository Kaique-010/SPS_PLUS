from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Licencas(models.Model):
    lice_id = models.AutoField('Id', primary_key=True)
    lice_docu = models.CharField('Documento', max_length=60, unique=True, blank=True, null=True)
    lice_nome = models.CharField('Nome Empresa', max_length=60, blank=True, null=True)
    lice_emai = models.EmailField('E-mail', max_length=150, blank=True, null=True)
    lice_bloq = models.BooleanField('Ativa?', default=False)
    lice_data_cria = models.DateField('Data de Criação', auto_now_add=True)

    class Meta:
        db_table = 'licencas'
        verbose_name = 'Licença'

    def __str__(self):
        return f"Licença {self.lice_id} - {self.lice_docu} - {self.lice_nome}"


class Empresas(models.Model):
    empr_id = models.AutoField(primary_key=True)
    empr_nome = models.CharField('Nome da Empresa', max_length=100)
    empr_docu = models.CharField('CNPJ', max_length=14, unique=True)
    empr_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True)
    empr_regi = models.CharField('Regime Tributação', max_length=50, choices=[
        ('simples_nacional', 'Simples Nacional'),
        ('regime_normal', 'Regime Normal')
    ])
    empr_cep = models.CharField('CEP', max_length=8)
    empr_ende = models.CharField('Endereço', max_length=100)
    empr_nume = models.CharField('Número', max_length=10)
    empr_esta = models.CharField('Estado', max_length=2)
    empr_bair = models.CharField('Bairro', max_length=100)
    empr_cida = models.CharField('Cidade', max_length=100)
    empr_emai = models.EmailField('E-mail', blank=True, null=True)
    
    licenca = models.ForeignKey(Licencas, on_delete=models.CASCADE, related_name="empresas")

    class Meta:
        db_table = 'empresas'
        unique_together = ('licenca', 'empr_docu')

    def __str__(self):
        return self.empr_nome


class Filiais(models.Model):
    fili_id = models.AutoField(primary_key=True)
    fili_nome = models.CharField('Nome da Filial', max_length=100)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='filiais')
    fili_docu = models.CharField('CNPJ', max_length=14, blank=True, null=True)
    fili_ie = models.CharField('Inscrição Estadual', max_length=11, blank=True, null=True)
    fili_regi = models.CharField('Regime Tributação', max_length=50, choices=[
        ('simples_nacional', 'Simples Nacional'),
        ('regime_normal', 'Regime Normal')
    ])
    fili_cep = models.CharField('CEP', max_length=8)
    fili_ende = models.CharField('Endereço', max_length=100)
    fili_nume = models.CharField('Número', max_length=10)
    fili_esta = models.CharField('Estado', max_length=2)
    fili_bair = models.CharField('Bairro', max_length=100)
    fili_cida = models.CharField('Cidade', max_length=100)
    fili_emai = models.EmailField('E-mail', blank=True, null=True)

    class Meta:
        db_table = 'filiais'
        unique_together = ('empresa', 'fili_docu')

    def __str__(self):
        return self.fili_nome


class UsuarioManager(BaseUserManager):
    def create_user(self, login, nome, email, password=None, **extra_fields):
        """
        Cria e retorna um usuário com login, nome, email e senha.
        """
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(login=login, nome=nome, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, nome, email, password=None, **extra_fields):
        """
        Cria e retorna um superusuário com login, nome, email e senha.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Atribuindo uma licença ao superusuário, mesmo que ele não precise de uma específica
        licenca = Licencas.objects.first()  # Pega a primeira licença no banco (ou escolha outra lógica)
        if licenca:
            extra_fields.setdefault('licenca', licenca)

        return self.create_user(login, nome, email, password, **extra_fields)


class Usuarios(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField("ID", primary_key=True)
    licenca = models.ForeignKey(Licencas, on_delete=models.CASCADE, related_name="usuarios")
    nome = models.CharField("Nome", max_length=100)
    login = models.CharField("Login", max_length=50, unique=True)
    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=[("M", "Masculino"), ("F", "Feminino")], blank=True, null=True)
    email = models.EmailField("E-mail", unique=True, max_length=100)
    telefone = models.CharField("Telefone", max_length=14, blank=True, null=True)
    ativo = models.BooleanField("Ativo?", default=True)

    empresas = models.ManyToManyField(Empresas, related_name="usuarios")
    filiais = models.ManyToManyField(Filiais, related_name="usuarios")

    is_staff = models.BooleanField(default=False)


    objects = UsuarioManager()
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["nome", "email"]

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return self.nome