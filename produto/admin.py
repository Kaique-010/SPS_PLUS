from django.contrib import admin
from .models import (
    GrupoProduto, SubgrupoProduto, FamiliaProduto, Marca,
    Produtos, Tabelaprecos, SaldoProduto
)


@admin.register(GrupoProduto)
class GrupoProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('descricao',)


@admin.register(SubgrupoProduto)
class SubgrupoProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('descricao',)


@admin.register(FamiliaProduto)
class FamiliaProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('descricao',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('nome',)


@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('prod_codi', 'prod_nome', 'prod_grup', 'prod_marc', 'imagem_tag')
    search_fields = ('prod_codi', 'prod_nome')
    list_filter = ('prod_grup', 'prod_marc')
    readonly_fields = ('imagem_tag',)


@admin.register(Tabelaprecos)
class TabelaprecosAdmin(admin.ModelAdmin):
    list_display = ('tabe_prod', 'tabe_prco', 'tabe_vare')
    search_fields = ('tabe_prod__prod_nome',)
    list_filter = ('tabe_empr', 'tabe_fili')


@admin.register(SaldoProduto)
class SaldoProdutoAdmin(admin.ModelAdmin):
    list_display = ('sapr_prod', 'sapr_sald')
    search_fields = ('sapr_prod__prod_nome',)
    list_filter = ('sapr_empr', 'sapr_fili')

