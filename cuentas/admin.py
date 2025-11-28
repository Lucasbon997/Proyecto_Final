from django.contrib import admin
from .models import Perfil, TarjetaRegalo


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "saldo")


@admin.register(TarjetaRegalo)
class TarjetaRegaloAdmin(admin.ModelAdmin):
    list_display = ("codigo", "monto", "usado", "usado_por", "fecha_creacion", "fecha_uso")
    search_fields = ("codigo", "usado_por__username")
    list_filter = ("usado",)


