from django.contrib import admin
from .models import DestacadoInicio


@admin.register(DestacadoInicio)
class DestacadoInicioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "es_oferta", "producto", "activo", "orden", "fecha_creacion")
    list_filter = ("es_oferta", "activo")
    search_fields = ("titulo", "descripcion_corta")
    ordering = ("orden",)
