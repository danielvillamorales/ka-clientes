from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import xlwt
from datetime import date

from ..models.venta_no_realizada import VentaNoRealizada
from ..models.bodega import Bodega
from ..models.color import Color
from ..models.genero import Genero
from ..models.motivo import Motivo
from ..models.producto import Producto
from ..models.silueta import Silueta
from ..models.talla import Talla

from ..forms import VentaNoRealizadaForm

def index(request):
    motivos = Motivo.objects.all()
    productos = Producto.objects.all()
    bodegas = Bodega.objects.all()
    colores = Color.objects.all()
    tallas = Talla.objects.all()
    siluetas = Silueta.objects.all()
    generos = Genero.objects.all()

    ventas_no_realizadas = aplicar_filtros(request)
    
    return render(request, "ventasapp/index.html", {
        "ventas_no_realizadas": ventas_no_realizadas,
        "motivos": motivos,
        "productos": productos,
        "bodegas":bodegas,
        "colores": colores,
        "tallas":tallas,
        "siluetas":siluetas,
        "generos": generos
    })

def aplicar_filtros(request):
    q = VentaNoRealizada.objects.all()

    if request.GET :
        fecha_desde = request.GET['fechaDesde'] 
        fecha_hasta = request.GET['fechaHasta']

        id_motivo =request.GET['id_motivo']
        id_producto = request.GET['id_producto']
        id_bodega = request.GET['id_bodega']
        id_color = request.GET['id_color']
        id_talla = request.GET['id_talla']
        id_silueta = request.GET['id_silueta']
        id_genero = request.GET['id_genero']

        if fecha_desde or fecha_hasta:        
            if fecha_desde and fecha_hasta:
                q = q.filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta)
            elif fecha_desde and not fecha_hasta:
                q = q.filter(fecha__gte=fecha_desde)
            else:
                q = q.filter(fecha__lte =fecha_hasta)
    
        if id_motivo:
            q = q.filter(motivo=id_motivo)

        if id_producto:
            q = q.filter(producto=id_producto)

        if id_bodega:
            q = q.filter(bodega=id_bodega)

        if id_color:
            q = q.filter(color=id_color)

        if id_talla:
            q = q.filter(talla=id_talla)

        if id_silueta:
            q = q.filter(silueta=id_silueta)

        if id_genero:
            q = q.filter(genero=id_genero)

    return q

def detalle_venta_no_realizada(request, venta_id):
    venta_no_realizada = get_object_or_404(VentaNoRealizada, pk=venta_id)
    return render(request, "ventasapp/detalle.html", {
        "venta_no_realizada": venta_no_realizada
    })

def editar_venta_no_realizada(request, venta_id):
    instancia = VentaNoRealizada.objects.get(id=venta_id)
    form = VentaNoRealizadaForm(instance=instancia)

    if request.method =='POST':

        form=VentaNoRealizadaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:index"))
    context = {'form': form}
    return render(request, "ventasapp/editar_movimiento.html", context)

def crear_venta_no_realizada(request):
    form = VentaNoRealizadaForm()

    if request.method == "POST":
        form = VentaNoRealizadaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:index"))
    context = {
        'form':form,
        }
    return render(request, "ventasapp/crear_movimiento.html", context)

def eliminar_movimiento(request, venta_id):
    movimiento = VentaNoRealizada.objects.get(id=venta_id)
    movimiento.delete()
    return HttpResponseRedirect(reverse("ventasapp:index"))

def exportar(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Movimientos') # Nombre del libro

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Fecha', 'Cod_Genero','Desc_Genero', 
                'Edad', 'Cod_Bodega','Desc_Bodega',
                'Cod_Producto', 'Desc_Producto',
                'Cod_Color', 'Desc_Color',
                'Cod_Talla', 'Desc_Talla', 'Cod_Silueta', 
                'Desc_Silueta', 'Cod_Motivo','Desc_Motivo',
                'Observacion']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = VentaNoRealizada.objects.all().values_list('fecha', 'genero__codigo', 'genero__descripcion', 
                                                        'edad', 'bodega__codigo', 'bodega__descripcion', 
                                                        'producto__codigo', 'producto__descripcion', 
                                                        'color__codigo', 'color__descripcion', 
                                                        'talla__codigo', 'talla__descripcion', 
                                                        'silueta__codigo', 'silueta__descripcion', 
                                                        'motivo__codigo', 'motivo__descripcion', 'observacion')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], date):
                fecha = row[col_num].strftime('%Y-%m-%d')
                ws.write(row_num, col_num, fecha, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    today    = date.today()
    strToday = today.strftime("%Y-%m-%d")

    nombre = "Movimiento_" + strToday + ".xls"

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' +nombre+''
    wb.save(response)

    return response

def listar_movimiento(request):
    ventas_no_realizadas = VentaNoRealizada.objects.all()
    return render(request, "ventasapp/listar_movimiento.html", {
        "ventas_no_realizadas": ventas_no_realizadas
    })
