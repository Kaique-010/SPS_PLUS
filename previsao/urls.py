from django.urls import path
from .views import previsao_estoque, prever_saldo

urlpatterns = [
    path("previsao/<int:produto_id>/<int:empresa_id>/<int:filial_id>/<int:licenca_id>/", previsao_estoque, name="previsao_estoque"),
    path("prever-saldo/", prever_saldo, name="prever_saldo"),
]
