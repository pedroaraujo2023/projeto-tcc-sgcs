from django.contrib import admin
from .models import Usuario, Chamado
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Registre o modelo de usuário padrão
admin.site.register(Usuario)

# Personalizar as permissões para o modelo Chamado
class ChamadoAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        # Apenas usuários autenticados podem visualizar Chamados
        return request.user.is_authenticated
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Use o site de administração personalizado para registrar Chamado
admin.site.register(Chamado, ChamadoAdmin)
