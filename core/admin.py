from django.contrib import admin
from .models import Carrera, PDF

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'materia', 'carrera')
    search_fields = ('nombre', 'codigo__nombre', 'id_carrera__nombre')
    list_filter = ('id_carrera',)

    def materia(self, obj):
        return obj.codigo.nombre if obj.codigo else None
    materia.admin_order_field = 'codigo__nombre'
    materia.short_description = 'Materia'

    def carrera(self, obj):
        return obj.id_carrera.nombre if obj.id_carrera else None
    carrera.admin_order_field = 'id_carrera__nombre'
    carrera.short_description = 'Carrera'
