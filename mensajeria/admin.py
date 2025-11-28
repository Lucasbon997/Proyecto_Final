from django.contrib import admin
from .models import SolicitudAmistad, Amistad, ChatMensaje

@admin.register(SolicitudAmistad)
class SolicitudAmistadAdmin(admin.ModelAdmin):
    list_display = ("de_usuario", "para_usuario", "estado", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("de_usuario__username", "para_usuario__username")


@admin.register(Amistad)
class AmistadAdmin(admin.ModelAdmin):
    list_display = ("usuario", "amigo", "fecha_desde")
    search_fields = ("usuario__username", "amigo__username")


@admin.register(ChatMensaje)
class ChatMensajeAdmin(admin.ModelAdmin):
    list_display = ("de_usuario", "para_usuario", "fecha_envio")
    search_fields = ("de_usuario__username", "para_usuario__username", "texto")
    list_filter = ("fecha_envio",)
