# urls.py
from django.urls import path
from .views import LicencasListView, LicencasCreateView, LicencasUpdateView, LicencasDetailView, LicencasDeleteView
from .views import (
    EmpresaListView, EmpresaCreateView, EmpresaUpdateView, EmpresaDetailView, EmpresaDeleteView,
    FilialListView, FilialCreateView, FilialUpdateView, FilialDetailView, FilialDeleteView, UsuarioCreateView
)

urlpatterns = [
    path('licencas/', LicencasListView.as_view(), name='licenca_list'),
    path('licenca/criar/', LicencasCreateView.as_view(), name='licenca_create'),
    path('licenca/editar/<int:pk>/', LicencasUpdateView.as_view(), name='licenca_update'),
    path('licenca/detalhar/<int:pk>/', LicencasDetailView.as_view(), name='licenca_detail'),
    path('licenca/excluir/<int:pk>/', LicencasDeleteView.as_view(), name='licenca_delete'),
    
    # URLs para Empresas
    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/criar/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/editar/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/detalhar/<int:pk>/', EmpresaDetailView.as_view(), name='empresa_detail'),
    path('empresa/excluir/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete'),

    # URLs para Filiais
    path('filiais/', FilialListView.as_view(), name='filial_list'),
    path('filial/criar/', FilialCreateView.as_view(), name='filial_create'),
    path('filial/editar/<int:pk>/', FilialUpdateView.as_view(), name='filial_update'),
    path('filial/detalhar/<int:pk>/', FilialDetailView.as_view(), name='filial_detail'),
    path('filial/excluir/<int:pk>/', FilialDeleteView.as_view(), name='filial_delete'),
    
    #usuarios
    path("usuario/", UsuarioCreateView.as_view(), name="usuario"),
]

