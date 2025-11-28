from django.db import models
from paginas.models import Pagina


class DestacadoInicio(models.Model):
    titulo = models.CharField("Título", max_length=150)
    descripcion_corta = models.CharField("Descripción corta", max_length=255)
    es_oferta = models.BooleanField(
        "¿Es una oferta?",
        default=False,
        help_text="Marcar si esta tarjeta corresponde a una oferta especial."
    )
    producto = models.ForeignKey(
        Pagina,
        verbose_name="Producto asociado",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Producto al que se redirige el botón de la tarjeta (opcional).",
        related_name="destacados_inicio",
    )
    imagen = models.ImageField(
        "Imagen (opcional)",
        upload_to="destacados/",
        blank=True,
        null=True
    )
    activo = models.BooleanField(
        "¿Mostrar en inicio?",
        default=True
    )
    orden = models.PositiveIntegerField(
        "Orden",
        default=0,
        help_text="Orden de aparición en inicio (0 primero)."
    )
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Destacado de inicio"
        verbose_name_plural = "Destacados de inicio"
        ordering = ["orden", "-fecha_creacion"]

    def __str__(self):
        return self.titulo
