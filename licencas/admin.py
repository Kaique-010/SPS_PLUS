from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios
from .forms import UsuarioForm

class UsuarioAdmin(UserAdmin):
    add_form = UsuarioForm  # Formulário para adicionar usuários
    model = Usuarios
    list_display = ("usua_nome", "usua_login", "usua_emai", "empresa", "filial", "usua_bloq", "is_superuser")
    list_filter = ("usua_bloq", "is_superuser")
    
    fieldsets = (
        ("Informações Pessoais", {"fields": ("usua_nome", "usua_login", "usua_emai", "usua_fone", "usua_data_nasc", "usua_sexo")}),
        ("Acesso", {"fields": ("password", "usua_bloq", "is_staff", "is_superuser")}),
        ("Permissões", {"fields": ("usua_libe_clie_bloq", "usua_libe_pedi_comp")}),
        ("Relacionamentos", {"fields": ("licenca", "empresa", "filial")}),
    )

    add_fieldsets = (
        ("Criar Novo Usuário", {
            "classes": ("wide",),
            "fields": ("usua_nome", "usua_login", "usua_emai", "password1", "password2", "usua_bloq"),
        }),
    )

    search_fields = ("usua_nome", "usua_login", "usua_emai")
    ordering = ("usua_nome",)
    filter_horizontal = ()

admin.site.register(Usuarios, UsuarioAdmin)
