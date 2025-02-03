from django.contrib import admin
from .models import Saida_Produtos

class Saida_ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto_codigo', 'entidade', 'quantidade', 'criado', 'modificado', 'id', 'documento')
    list_filter = ('criado', 'modificado', 'produto_codigo', 'quantidade')

admin.site.register(Saida_Produtos, Saida_ProdutosAdmin)