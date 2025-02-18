from django.urls import path
from . import views
from .views import (
    OrcamentoListView,
    OrcamentoCreateView,
    OrcamentoUpdateView,
    OrcamentoDetailView,
    OrcamentoDeleteView,

)

urlpatterns = [
    path("orcamentos/", OrcamentoListView.as_view(), name="orcamento_list"),
    path("novo/", OrcamentoCreateView.as_view(), name="orcamento_form"),
    path("<int:pk>/editar/", OrcamentoUpdateView.as_view(), name="orcamento_update"),
    path("<int:pk>/", OrcamentoDetailView.as_view(), name="orcamento_detail"),
    path("<int:pk>/excluir/", OrcamentoDeleteView.as_view(), name="orcamento_delete"),
    path('buscar_produtos/', views.buscar_produtos, name='buscar_produtos'),
]
