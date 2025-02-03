
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import saldo

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include ('Entidades.urls')),
    path('', include('Pedidos.urls')),
    path('', include ('Produtos.urls')),
    path('', include ('Financeiro.urls')),
    #path('', include ('Ordem_de_servico.urls')),
    #path('', include ('Ordemproducao.urls')),
    path('', include ('orcamentos.urls')),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)