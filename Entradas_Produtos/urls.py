from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

appname= 'Entradas_Produtos'

urlpatterns = [
    path('entradas/lista/', views.EntradasListView.as_view(), name='entradaslistas'),
    path('entradas/criar/', views.EntradasCreateView.as_view(), name='entradascriar'),
    path('entradas/<int:pk>/detalhes/', views.EntradasDetailView.as_view(), name='entradasdetalhe'),
    path('entradas/<int:pk>/editar/', views.EntradasUpdateView.as_view(), name='entradaseditar'),
    path('entradas/<int:pk>/excluir/', views.EntradasDeleteView.as_view(), name='entradasexcluir'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
