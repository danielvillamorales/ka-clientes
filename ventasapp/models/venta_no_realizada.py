from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from . import Bodega, Genero, Motivo, Producto, Color, Talla, Silueta

class VentaNoRealizada(models.Model):
    fecha = models.DateField()
    bodega = models.ForeignKey(
        Bodega, 
        on_delete=models.CASCADE
    )

    edad = models.SmallIntegerField(
        blank=True,
        null=True,
    )

    genero = models.ForeignKey(
        Genero, 
        on_delete=models.CASCADE
    )

    motivo = models.ForeignKey(
        Motivo,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )

    talla = models.ForeignKey(
        Talla, 
        on_delete=models.CASCADE
    )

    silueta = models.ForeignKey(
        Silueta,
        on_delete=models.CASCADE
    )

    observacion = models.TextField(
        blank=True, 
        null=True
    )

    def __str__(self):
        return str(self.fecha) + " - " + self.observacion
