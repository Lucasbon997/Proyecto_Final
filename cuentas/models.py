from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatares/", blank=True, null=True)
    biografia = models.TextField(blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class TarjetaRegalo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    usado = models.BooleanField(default=False)
    usado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tarjetas_usadas",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        estado = "Usada" if self.usado else "Disponible"
        return f"{self.codigo} - {self.monto} ({estado})"
