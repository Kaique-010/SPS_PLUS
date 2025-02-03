from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

appname= 'saidas'

urlpatterns = [
    path('saidas/lista/', views.SaidasListView.as_view(), name='saidaslistas'),
    path('saidas/criar/', views.SaidasCreateView.as_view(), name='saidascriar'),
    path('saidas/<int:pk>/detalhes/', views.SaidasDetailView.as_view(), name='saidasdetalhe'),
    path('saidas/<int:pk>/editar/', views.SaidasUpdateView.as_view(), name='saidaseditar'),
    path('saidas/<int:pk>/excluir/', views.SaidasDeleteView.as_view(), name='saidasexcluir'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
