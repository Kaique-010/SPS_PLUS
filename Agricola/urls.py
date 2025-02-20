from django.urls import path
from .views import (
    FazendaListView, FazendaCreateView, FazendaUpdateView, FazendaDeleteView, RelatorioMovimentacoesView,
    TalhaoListView, TalhaoCreateView, TalhaoUpdateView, TalhaoDeleteView,
    ProdutoAgroListView, ProdutoAgroCreateView, ProdutoAgroUpdateView, ProdutoAgroDeleteView,
    EstoqueFazendaListView, EstoqueFazendaCreateView, EstoqueFazendaUpdateView, EstoqueFazendaDeleteView,
    MovimentacaoEstoqueListView, MovimentacaoEstoqueCreateView, MovimentacaoEstoqueUpdateView, MovimentacaoEstoqueDeleteView,
    AplicacaoInsumosListView, AplicacaoInsumosCreateView, AplicacaoInsumosUpdateView, AplicacaoInsumosDeleteView,
    AnimalListView, AnimalCreateView, AnimalUpdateView, AnimalDeleteView,
    EventoAnimalListView, EventoAnimalCreateView, EventoAnimalUpdateView, EventoAnimalDeleteView,
    CicloFlorestalListView, CicloFlorestalCreateView, CicloFlorestalUpdateView, CicloFlorestalDeleteView,
    CategoriaProdutoListView,CategoriaProdutoCreateView,CategoriaProdutoUpdateView,CategoriaProdutoDeleteView,
)


urlpatterns = [
    path("fazendas/", FazendaListView.as_view(), name="fazenda_list"),
    path("fazendas/nova/", FazendaCreateView.as_view(), name="fazenda_form"),
    path("fazendas/<int:pk>/editar/", FazendaUpdateView.as_view(), name="fazenda_update"),
    path("fazendas/<int:pk>/deletar/", FazendaDeleteView.as_view(), name="fazenda_delete"),

    path("talhoes/", TalhaoListView.as_view(), name="talhao_list"),
    path("talhoes/novo/", TalhaoCreateView.as_view(), name="talhao_form"),
    path("talhoes/<int:pk>/editar/", TalhaoUpdateView.as_view(), name="talhao_update"),
    path("talhoes/<int:pk>/deletar/", TalhaoDeleteView.as_view(), name="talhao_delete"),
    
    path('categorias/', CategoriaProdutoListView.as_view(), name='categoria_produto_list'),
    path('categorias/novo/', CategoriaProdutoCreateView.as_view(), name='categoria_produto_form'),
    path('categorias/editar/<int:pk>/', CategoriaProdutoUpdateView.as_view(), name='categoria_produto_update'),
    path('categorias/excluir/<int:pk>/', CategoriaProdutoDeleteView.as_view(), name='categoria_produto_delete'),

    path("produtos/", ProdutoAgroListView.as_view(), name="produtoagro_list"),
    path("produtos/novo/", ProdutoAgroCreateView.as_view(), name="produtoagro_form"),
    path("produtos/<int:pk>/editar/", ProdutoAgroUpdateView.as_view(), name="produtoagro_update"),
    path("produtos/<int:pk>/deletar/", ProdutoAgroDeleteView.as_view(), name="produtoagro_delete"),

    path("estoques/", EstoqueFazendaListView.as_view(), name="estoquefazenda_list"),
    path("estoques/novo/", EstoqueFazendaCreateView.as_view(), name="estoquefazenda_form"),
    path("estoques/<int:pk>/editar/", EstoqueFazendaUpdateView.as_view(), name="estoquefazenda_update"),
    path("estoques/<int:pk>/deletar/", EstoqueFazendaDeleteView.as_view(), name="estoquefazenda_delete"),

    path("movimentacoes/", MovimentacaoEstoqueListView.as_view(), name="movimentacaoestoque_list"),
    path("movimentacoes/nova/", MovimentacaoEstoqueCreateView.as_view(), name="movimentacaoestoque_form"),
    path("movimentacoes/<int:pk>/editar/", MovimentacaoEstoqueUpdateView.as_view(), name="movimentacaoestoque_update"),
    path("movimentacoes/<int:pk>/deletar/", MovimentacaoEstoqueDeleteView.as_view(), name="movimentacaoestoque_delete"),

    path("aplicacoes/", AplicacaoInsumosListView.as_view(), name="aplicacaoinsumos_list"),
    path("aplicacoes/nova/", AplicacaoInsumosCreateView.as_view(), name="aplicacaoinsumos_form"),
    path("aplicacoes/<int:pk>/editar/", AplicacaoInsumosUpdateView.as_view(), name="aplicacaoinsumos_update"),
    path("aplicacoes/<int:pk>/deletar/", AplicacaoInsumosDeleteView.as_view(), name="aplicacaoinsumos_delete"),

    path("animais/", AnimalListView.as_view(), name="animal_list"),
    path("animais/novo/", AnimalCreateView.as_view(), name="animal_form"),
    path("animais/<int:pk>/editar/", AnimalUpdateView.as_view(), name="animal_update"),
    path("animais/<int:pk>/deletar/", AnimalDeleteView.as_view(), name="animal_delete"),

    path("eventos/", EventoAnimalListView.as_view(), name="eventoanimal_list"),
    path("eventos/novo/", EventoAnimalCreateView.as_view(), name="eventoanimal_form"),
    path("eventos/<int:pk>/editar/", EventoAnimalUpdateView.as_view(), name="eventoanimal_update"),
    path("eventos/<int:pk>/deletar/", EventoAnimalDeleteView.as_view(), name="eventoanimal_delete"),

    path("ciclos/", CicloFlorestalListView.as_view(), name="cicloflorestal_list"),
    path("ciclos/novo/", CicloFlorestalCreateView.as_view(), name="cicloflorestal_form"),
    path("ciclos/<int:pk>/editar/", CicloFlorestalUpdateView.as_view(), name="cicloflorestal_update"),
    path("ciclos/<int:pk>/deletar/", CicloFlorestalDeleteView.as_view(), name="cicloflorestal_delete"),
    
    path('movimentacoes/', RelatorioMovimentacoesView.as_view(), name='movimentacoes_list'),
]
