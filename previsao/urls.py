from django.urls import path
from . import views

urlpatterns = [
    path('previsao-estoque/<int:produto_id>/<int:empresa_id>/<int:filial_id>/<int:licenca_id>/', views.previsao_estoque, name='previsao_estoque'),
]
