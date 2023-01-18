from django.contrib import admin

from .models import Bodega, Color, Genero, Motivo, Producto, Silueta, Talla, VentaNoRealizada

admin.site.register(Bodega)
admin.site.register(Color)
admin.site.register(Genero)
admin.site.register(Motivo)
admin.site.register(Producto)
admin.site.register(Silueta)
admin.site.register(Talla)
admin.site.register(VentaNoRealizada)

