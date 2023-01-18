from django.urls import path
from .views.ventas_view import index, detalle_venta_no_realizada, editar_venta_no_realizada, crear_venta_no_realizada, eliminar_movimiento, exportar, listar_movimiento
from .views.bodega_view import bodegas, crear_bodega, editar_bodega, eliminar_bodega
from .views.color_view import colores, crear_color, editar_color, eliminar_color
from .views.genero_view import generos, crear_genero, editar_genero, eliminar_genero
from .views.motivo_view import motivos, crear_motivo, editar_motivo, eliminar_motivo
from .views.producto_view import productos, crear_producto, editar_producto, eliminar_producto
from .views.silueta_view import siluetas, crear_silueta, editar_silueta, eliminar_silueta
from .views.talla_view import tallas, crear_talla, editar_talla, eliminar_talla

app_name= "ventasapp"
urlpatterns = [
    path("", index, name="index"), 
    path("<int:venta_id>/ver/", detalle_venta_no_realizada, name="detalle"),
    path("<int:venta_id>/editar/", editar_venta_no_realizada, name="editar"),
    path("crear/", crear_venta_no_realizada, name="crear_venta_no_realizada"),
    path("<int:venta_id>/eliminar", eliminar_movimiento, name="eliminar_movimiento"),

    path("exportar", exportar, name="exportar"),
    path("listar_movimiento", listar_movimiento, name="listar_movimiento"),

    path("bodegas/", bodegas, name="detalle_bodegas"),
    path("bodegas/crear", crear_bodega, name="crear_bodega"),
    path("bodegas/<int:bodega_id>/editar", editar_bodega, name="editar_bodega"),
    path("bodegas/<int:bodega_id>/eliminar", eliminar_bodega, name="eliminar_bodega"),

    path("colores/", colores, name="detalle_colores"),
    path("colores/crear", crear_color, name="crear_color"),
    path("colores/<int:color_id>/editar", editar_color, name="editar_color"),
    path("colores/<int:color_id>/eliminar", eliminar_color, name="eliminar_color"),

    path("generos/", generos, name="detalle_generos"),
    path("generos/crear", crear_genero, name="crear_genero"),
    path("generos/<int:genero_id>/editar", editar_genero, name="editar_genero"),
    path("generos/<int:genero_id>/eliminar", eliminar_genero, name="eliminar_genero"),

    path("motivos/", motivos, name="detalle_motivos"),
    path("motivos/crear", crear_motivo, name="crear_motivo"),
    path("motivos/<int:motivo_id>/editar", editar_motivo, name="editar_motivo"),
    path("motivos/<int:motivo_id>/eliminar", eliminar_motivo, name="eliminar_motivo"),

    path("productos/", productos, name="detalle_productos"),
    path("productos/crear", crear_producto, name="crear_producto"),
    path("productos/<int:producto_id>/editar", editar_producto, name="editar_producto"),
    path("productos/<int:producto_id>/eliminar", eliminar_producto, name="eliminar_producto"),

    path("siluetas/", siluetas, name="detalle_siluetas"),
    path("siluetas/crear", crear_silueta, name="crear_silueta"),
    path("siluetas/<int:silueta_id>/editar", editar_silueta, name="editar_silueta"),
    path("siluetas/<int:silueta_id>/eliminar", eliminar_silueta, name="eliminar_silueta"),

    path("tallas/", tallas, name="detalle_tallas"),
    path("tallas/crear", crear_talla, name="crear_talla"),
    path("tallas/<int:talla_id>/editar", editar_talla, name="editar_talla"),
    path("tallas/<int:talla_id>/eliminar", eliminar_talla, name="eliminar_talla"),
]
