from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes_enviados")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes_recibidos")
    asunto = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asunto} ({self.remitente} → {self.destinatario})"



class SolicitudAmistad(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("aceptada", "Aceptada"),
        ("rechazada", "Rechazada"),
    )

    de_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="solicitudes_enviadas",
    )
    para_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="solicitudes_recibidas",
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="pendiente",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud de amistad"
        verbose_name_plural = "Solicitudes de amistad"
        unique_together = ("de_usuario", "para_usuario")

    def __str__(self):
        return f"{self.de_usuario.username} → {self.para_usuario.username} ({self.estado})"


class Amistad(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="amistades",
    )
    amigo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="amigos_de",
    )
    fecha_desde = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Amistad"
        verbose_name_plural = "Amistades"
        unique_together = ("usuario", "amigo")

    def __str__(self):
        return f"{self.usuario.username} ↔ {self.amigo.username}"


class ChatMensaje(models.Model):
    de_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats_enviados",
    )
    para_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats_recibidos",
    )
    texto = models.TextField("Mensaje")
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje de chat"
        verbose_name_plural = "Mensajes de chat"
        ordering = ["fecha_envio"]

    def __str__(self):
        return f"Chat {self.de_usuario.username} → {self.para_usuario.username}: {self.texto[:30]}"
