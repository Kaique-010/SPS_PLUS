from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EntidadesViewSet,EntidadeUpdateView,entidade_delete,exportar_entidades)
from .views import EntidadeCreateView, EntidadesListView

router = DefaultRouter()
router.register(r'entidades', EntidadesViewSet)

urlpatterns = [
    # Rotas para a API
    path('api/', include(router.urls)),

   
    path('entidades/', EntidadesListView.as_view(), name='entidades'),
    path('entidade/create/', EntidadeCreateView.as_view(), name='entidade_form'),
    path('entidade/update/<str:enti_clie>/', EntidadeUpdateView.as_view(), name='entidade_update'),
    path('entidade/delete/<str:enti_clie>/', entidade_delete, name='entidade_delete'),
    
    
    
    path('exportar/', exportar_entidades, name='exportar_entidades'),
]
