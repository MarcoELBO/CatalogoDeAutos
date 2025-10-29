from django.contrib import admin
from .models import Usuario, Vendedor, Auto, Consulta, Resena
# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')
    search_fields = ('nombre', )

class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'email', 'telefono')
    search_fields = ('nombre', 'email')

class AutoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'anio', 'precio', 'vendedor', 'estado')
    list_filter = ('estado','marca', 'anio', 'vendedor')
    search_fields = ('marca', 'modelo', 'version')

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('auto', 'usuario', 'fecha_consulta')
    list_filter = ('fecha_consulta',)

class ResenaAdmin(admin.ModelAdmin):
    list_display = ('auto', 'usuario', 'puntuacion', 'fecha_resena')
    list_filter = ('puntuacion', 'fecha_resena',)

#Registrar los modelos en el admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Resena, ResenaAdmin)


