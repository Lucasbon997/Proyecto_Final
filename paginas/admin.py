from django.contrib import admin
from .models import Categoria, Pagina, Compra, Reseña

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fecha_publicacion", "categoria", "precio")
    search_fields = ("titulo", "subtitulo", "autor__username", "categoria__nombre")
    list_filter = ("categoria", "fecha_publicacion")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("usuario", "producto", "precio_pagado", "fecha_compra", "licencia")
    list_filter = ("fecha_compra", "producto")
    search_fields = ("usuario__username", "producto__titulo", "licencia")


@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ("producto", "usuario", "me_gusta", "fecha_creacion")
    list_filter = ("me_gusta", "fecha_creacion")
    search_fields = ("producto__titulo", "usuario__username", "texto")
