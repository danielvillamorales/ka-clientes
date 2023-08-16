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
    

class VentasClientesPsv(models.Model):
    ms_nit = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    anio = models.CharField(max_length=12, db_collation='USING_NLS_COMP', blank=True, null=True)
    documento = models.IntegerField(blank=True, null=True)
    ms_transaccion = models.CharField(max_length=44, db_collation='USING_NLS_COMP', blank=True, null=True)
    md_bodega = models.CharField(max_length=3, db_collation='USING_NLS_COMP', blank=True, null=True)
    vendido = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ventas_clientes_psv'
        app_label = 'logistica_db'
    
    def __str__(self) -> str:
        return f'nit: {self.ms_nit} - fecha: {self.fecha} - documento: {self.documento} - transaccion: {self.ms_transaccion} - bodega: {self.md_bodega} - vendido: {self.vendido} |'