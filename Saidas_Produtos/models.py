from django.db import models
from Entidades.models import Entidades
from produto.models import Produtos

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True) 
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True  


class Saida_Produtos(Base):
    data = models.DateField('Data Saída',null=True, blank=True)
    entidade = models.ForeignKey(Entidades, on_delete=models.PROTECT, blank=False, null=False, related_name= 'saidas')
    produto_codigo = models.ForeignKey(Produtos, on_delete=models.PROTECT, blank=False, null=False, related_name='saidas')
    quantidade = models.IntegerField()
    documento = models.CharField('Nº Documento', max_length= 20, blank= True, null= True)
    observacoes = models.TextField('Observações', max_length=200, blank= True, null= True)

    class Meta:
        ordering = ['-criado']

    class Meta:
        verbose_name = 'Saída Produto'
        verbose_name_plural = 'Saída Produtos'

def __str__(self):
    return str(self.produto_codigo)