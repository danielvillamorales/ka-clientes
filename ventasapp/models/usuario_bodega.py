from django.db import models

from .bodega import Bodega
from django.contrib.auth.models import User

class Usuario_Bodega(models.Model):
    bodega = models.OneToOneField(
        Bodega,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.usuario.username + ' ' + self.bodega.codigo
