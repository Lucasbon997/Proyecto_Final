from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Pagina(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paginas"
    )
    contenido = RichTextUploadingField()
    imagen = models.ImageField(upload_to="paginas/", blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.titulo



class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compras")
    producto = models.ForeignKey(Pagina, on_delete=models.CASCADE, related_name="compras")
    fecha_compra = models.DateTimeField(auto_now_add=True)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    licencia = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"Compra de {self.producto.titulo} por {self.usuario.username}"


class Reseña(models.Model):
    producto = models.ForeignKey(
        Pagina,
        on_delete=models.CASCADE,
        related_name="reseñas"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reseñas"
    )
    texto = models.TextField("Reseña")
    me_gusta = models.BooleanField(
        "¿Te gustó?",
        help_text="Marca si te gustó el producto."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-fecha_creacion"]
        unique_together = ("producto", "usuario")

    def __str__(self):
        estado = "👍 Me gustó" if self.me_gusta else "👎 No me gustó"
        return f"Reseña de {self.usuario.username} sobre {self.producto.titulo} ({estado})"

