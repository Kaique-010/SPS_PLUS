from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import pedidos_por_cliente, pedidos_necessitam_contato_view, marcar_contato_realizado, detalhar_contato,dashboard #criar_pedido
from Menu import views
from Pedidos import views
from .views import (
    PedidoVendaCreateView, 
    PedidoVendaUpdateView, 
    PedidoDetailView, 
    PedidoDeleteView, 
    
)

router = DefaultRouter()



urlpatterns = [

    path('api/pedidos', include(router.urls)),
    path('pedidos/por-cliente/', pedidos_por_cliente, name='pedidos_por_cliente'),
    path('pedidos-necessitam-contato/', pedidos_necessitam_contato_view, name='pedidos_necessitam_contato'),
    path('marcar-contato-realizado/<int:pedido_id>/', marcar_contato_realizado, name='marcar_contato_realizado'),
    path('detalhar_contato/<int:pedido_id>/', views.detalhar_contato, name='detalhar_contato'),
    path('detalhar_cliente/', detalhar_contato, name='detalhes_cliente'),
    path('dashboard/', dashboard, name='dashboard'),
    #path('pedido/', criar_pedido, name='pedidocriar.html'),
    path('pedido/', PedidoVendaCreateView.as_view(), name='pedidocriar.html'),
    path('pedidos/<int:pk>/editar/', PedidoVendaUpdateView.as_view(), name='pedido_editar'),
    path('pedidos/<int:pk>/detalhes/', PedidoDetailView.as_view(), name='pedido_detalhe'),
    path('pedidos/<int:pk>/excluir/', PedidoDeleteView.as_view(), name='pedido_excluir'),
    
]
