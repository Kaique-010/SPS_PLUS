from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutosViewSet, exportar_produtos,ProdutoListView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView
from .views import GrupoListView, GrupoCreateView, GrupoUpdateView, GrupoDeleteView
from .views import SubgrupoListView, SubgrupoCreateView, SubgrupoUpdateView, SubgrupoDeleteView
from .views import (
    MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView,
    FamiliaProdutoListView, FamiliaProdutoCreateView, FamiliaProdutoUpdateView, FamiliaProdutoDeleteView,saldo
)


# Cria um router para o EntidadesViewSet
router = DefaultRouter()
router.register(r'produtos', ProdutosViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('produtos_lista', ProdutoListView.as_view(), name='produtos_lista.html'),
    path('produto/create/', ProdutoCreateView.as_view(), name='produto_create'),
    path('produto/update/<str:prod_codi>/', ProdutoUpdateView.as_view(), name='produtos_update'),
    path('produto/delete/<str:prod_codi>/', ProdutoDeleteView.as_view(), name='produto_delete'),
    path('exportar-produtos/',exportar_produtos, name='exportar_produtos'),
    
    path('grupos_list', GrupoListView.as_view(), name='grupos_list'),
    path('grupo_create/', GrupoCreateView.as_view(), name='grupo_create'),
    path('grupo_update/<int:pk>/', GrupoUpdateView.as_view(), name='grupo_update'),
    path('grupo_delete/<int:pk>/', GrupoDeleteView.as_view(), name='grupo_delete'),
    
    path('subgrupos_list', SubgrupoListView.as_view(), name='subgrupos_list'),
    path('subgrupo_create/', SubgrupoCreateView.as_view(), name='subgrupo_create'),
    path('subgrupo_update/<int:pk>/', SubgrupoUpdateView.as_view(), name='subgrupo_update'),
    path('subgrupo_delete/<int:pk>/', SubgrupoDeleteView.as_view(), name='subgrupo_delete'),
    
    path('marcas/', MarcaListView.as_view(), name='marcas_list'),
    path('marcas/novo/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/editar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/deletar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_delete'),

    # URLs para FamiliaProduto
    path('familias/', FamiliaProdutoListView.as_view(), name='familias_produto_list'),
    path('familias/novo/', FamiliaProdutoCreateView.as_view(), name='familia_produto_create'),
    path('familias/editar/<int:pk>/', FamiliaProdutoUpdateView.as_view(), name='familia_produto_update'),
    path('familias/deletar/<int:pk>/', FamiliaProdutoDeleteView.as_view(), name='familia_produto_delete'),
    
    path('saldos/', saldo, name='saldo'), 
] 
# Servindo arquivos de mídia em modo de depuração
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)