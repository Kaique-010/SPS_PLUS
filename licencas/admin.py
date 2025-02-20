from django.contrib import admin
from .models import Usuarios

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('login', 'nome', 'email', 'ativo')  # Ajuste para 'login' no lugar de 'username'
    ordering = ['login']  # Ajuste para 'login'
    list_filter = ['ativo']  # Ajuste para 'ativo' no lugar de 'is_active'
    
    # Se desejar, você pode adicionar ações customizadas ou campos adicionais aqui
    # search_fields = ['login', 'nome', 'email']
    
admin.site.register(Usuarios, UsuarioAdmin)
