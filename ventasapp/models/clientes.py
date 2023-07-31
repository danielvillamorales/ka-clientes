from django.db import models
from ventasapp.models.bodega import Bodega


class Cliente(models.Model):
    nombre = models.CharField(max_length=250, null=False)
    cedula = models.CharField(max_length=30, null=False)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=250, null=True, blank=True)
    fecha_llamada = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ('listar_todos_clientes', 'listar_todos_clientes'),
            ('importar_clientes', 'importar_clientes')
        ]

    def __str__(self):
        return f'{self.nombre} - {self.cedula} - {self.bodega} - subido el {self.fecha_subida} - {self.observaciones} - {self.fecha_llamada}'
    