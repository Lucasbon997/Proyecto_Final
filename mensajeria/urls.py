from django.urls import path
from . import views

app_name = "mensajeria"

urlpatterns = [
    path("", views.bandeja_entrada, name="bandeja_entrada"),
    path("nuevo/", views.nuevo_mensaje, name="nuevo_mensaje"),
    path("<int:pk>/", views.detalle_mensaje, name="detalle_mensaje"),
    path("amigos/", views.lista_amigos, name="lista_amigos"),
    path("amigos/buscar/", views.buscar_usuarios, name="buscar_usuarios"),
    path("amigos/solicitar/<int:usuario_id>/", views.enviar_solicitud_amistad, name="enviar_solicitud_amistad"),
    path("amigos/solicitud/<int:solicitud_id>/<str:accion>/", views.responder_solicitud_amistad, name="responder_solicitud_amistad"),
    path("chat/<int:amigo_id>/", views.chat_con_amigo, name="chat_con_amigo"),
]
