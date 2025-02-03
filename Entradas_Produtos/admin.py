from django.contrib import admin
from .models import Entrada_Produtos

class Entrada_ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto_codigo', 'entidade', 'quantidade', 'criado', 'modificado', 'id', 'documento')
    list_filter = ('criado', 'modificado', 'produto_codigo', 'quantidade')

admin.site.register(Entrada_Produtos, Entrada_ProdutosAdmin)