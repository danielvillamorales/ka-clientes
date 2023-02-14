from django.db import models

class Genero(models.Model):
    codigo = models.CharField(
        max_length=30
    )

    descripcion = models.CharField(
        max_length=250,
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return str(self.codigo)
