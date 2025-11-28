from django.urls import path
from .views import (
    registrarse,
    ingresar,
    salir,
    perfil,
    editar_perfil,
    cambiar_password,
    recargar_saldo_tarjeta_regalo,
    recargar_saldo_tarjeta,
)

app_name = "cuentas"

urlpatterns = [
    path("registrarse/", registrarse, name="registrarse"),
    path("ingresar/", ingresar, name="ingresar"),
    path("salir/", salir, name="salir"),
    path("perfil/", perfil, name="perfil"),
    path("perfil/editar/", editar_perfil, name="editar_perfil"),
    path("perfil/password/", cambiar_password, name="cambiar_password"),
    path("perfil/saldo/regalo/", recargar_saldo_tarjeta_regalo, name="recargar_saldo_regalo"),
    path("perfil/saldo/tarjeta/", recargar_saldo_tarjeta, name="recargar_saldo_tarjeta"),
]
