
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django import views
from Menu import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include ('Entidades.urls')),
    path('', include('Pedidos.urls')),
    path('', include ('produto.urls')),
    path('', include ('Ordemservico.urls')),
    #path('', include ('Ordemproducao.urls')),
    path('', include ('Entradas_Produtos.urls')),
    path('', include ('Saidas_Produtos.urls')),
    path('', include ('orcamentos.urls')),
    path('', include ('licencas.urls')),
    path('', include ('IA.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
