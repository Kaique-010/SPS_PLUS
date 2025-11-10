from django.contrib import admin
from .models import Usuarios

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usua_codi')  # Ajuste para 'login' no lugar de 'username'
    ordering = ['nome']  # Ajuste para 'login'

    
    # Se desejar, você pode adicionar ações customizadas ou campos adicionais aqui
    # search_fields = ['login', 'nome', 'email']
    
admin.site.register(Usuarios, UsuarioAdmin)
