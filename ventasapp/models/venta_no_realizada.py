from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

from ventasapp.models.bodega import Bodega
from ventasapp.models.color import Color
from ventasapp.models.genero import Genero
from ventasapp.models.motivo import Motivo
from ventasapp.models.producto import Producto
from ventasapp.models.silueta import Silueta
from ventasapp.models.talla import Talla
from ventasapp.models.usuario_bodega import Usuario_Bodega
from ventasapp.models.material import Material
from ventasapp.models.diseno import Diseno

class VentaNoRealizada(models.Model):
    fecha = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    edad = models.SmallIntegerField(
        blank=True,
        null=True,
    )

    genero = models.ForeignKey(
        Genero, 
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    motivo = models.ForeignKey(
        Motivo,
        on_delete=models.PROTECT
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    talla = models.ForeignKey(
        Talla, 
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    silueta = models.ForeignKey(
        Silueta,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    diseno = models.ForeignKey(
        Diseno,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    ) 

    observacion = models.TextField(
        blank=True, 
        null=True
    )

    def __str__(self):
        return str(self.fecha) + " - " + self.observacion
