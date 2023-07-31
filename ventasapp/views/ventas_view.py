from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import xlwt
from datetime import date
from django.core.paginator import Paginator

from ..models.venta_no_realizada import VentaNoRealizada
from ..models.bodega import Bodega
from ..models.color import Color
from ..models.genero import Genero
from ..models.motivo import Motivo
from ..models.producto import Producto
from ..models.silueta import Silueta
from ..models.talla import Talla

from ..forms import VentaNoRealizadaForm
from ..models.usuario_bodega import Usuario_Bodega

from .utils import usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar, usuario_puede_listar

@login_required(login_url='ventasapp:login')
def index(request):
    modelo = "ventanorealizada"
    ventas_no_realizadas = None
    motivos = None
    productos = None
    bodegas = None
    colores = None
    tallas = None
    siluetas = None
    generos = None
    mensaje_error = None

    try:
        bodega = Usuario_Bodega.objects.get(usuario=request.user.id)
    except Usuario_Bodega.DoesNotExist:
        mensaje_error = 'Usuario no tiene bodega asociada'

    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request, modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        motivos = Motivo.objects.all().order_by('descripcion')
        productos = Producto.objects.all().order_by('descripcion')
        bodegas = Bodega.objects.all().order_by('descripcion')
        colores = Color.objects.all().order_by('descripcion')
        tallas = Talla.objects.all().order_by('descripcion')
        siluetas = Silueta.objects.all().order_by('descripcion')
        generos = Genero.objects.all().order_by('descripcion')

        ventas_no_realizadas = aplicar_filtros(request)
        paginator = Paginator(ventas_no_realizadas, 18)  # Cambiar el número "10" por la cantidad de elementos que deseas mostrar por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    return render(request, "ventasapp/index.html", {
        "ventas_no_realizadas": page_obj,
        "motivos": motivos,
        "productos": productos,
        "bodegas":bodegas,
        "colores": colores,
        "tallas":tallas,
        "siluetas":siluetas,
        "generos": generos,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar,
        "puede_listar": puede_listar,
        "mensaje_error": mensaje_error
    })

@login_required(login_url='ventasapp:login')
def aplicar_filtros(request):
    q = VentaNoRealizada.objects.all().order_by('-fecha')

    if request.GET :
        fecha_desde = request.GET.get('fechaDesde', None)
        fecha_hasta = request.GET.get('fechaHasta', None)

        id_motivo =request.GET.get('id_motivo', None)
        id_producto = request.GET.get('id_producto', None)
        id_bodega = request.GET.get('id_bodega', None)
        id_color = request.GET.get('id_color', None)
        id_talla = request.GET.get('id_talla', None)
        id_silueta = request.GET.get('id_silueta', None)
        id_genero = request.GET.get('id_genero', None)

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

@login_required(login_url='ventasapp:login')
def detalle_venta_no_realizada(request, venta_id):
    venta_no_realizada = get_object_or_404(VentaNoRealizada, pk=venta_id)
    return render(request, "ventasapp/detalle.html", {
        "venta_no_realizada": venta_no_realizada
    })

@login_required(login_url='ventasapp:login')
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

@login_required(login_url='ventasapp:login')
def crear_venta_no_realizada(request):
    try:
        bodega = Usuario_Bodega.objects.get(usuario=request.user.id)
    except Usuario_Bodega.DoesNotExist:
        return HttpResponseRedirect(reverse("ventasapp:index"))

    form = VentaNoRealizadaForm()

    if request.method == "POST":
        form = VentaNoRealizadaForm(request.POST)
        if form.is_valid():
            pk = form.save()
            agregar_movimiento_bodega_usuario(pk.id, request.user.id)
            return HttpResponseRedirect(reverse("ventasapp:index"))
    context = {
        'form':form,
        }
    return render(request, "ventasapp/crear_movimiento.html", context)

def agregar_movimiento_bodega_usuario(id_movimiento, usuario_id):
    bodega = Usuario_Bodega.objects.get(usuario=usuario_id)

    movimiento = VentaNoRealizada.objects.get(pk=id_movimiento)
    movimiento.bodega_id = bodega.bodega.id
    movimiento.save()


@login_required(login_url='ventasapp:login')
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

    columns = ['Fecha', 'Cod_Bodega','Desc_Bodega','Cod_Genero','Desc_Genero', 
                'Edad', 
                'Cod_Producto', 'Desc_Producto',
                'Cod_Color', 'Desc_Color',
                'Cod_Talla', 'Desc_Talla', 'Cod_Silueta', 
                'Desc_Silueta', 'Cod_Motivo','Desc_Motivo','Cod_Material','Material','Cod_Diseno','Diseno',
                'Observacion']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = VentaNoRealizada.objects.all().values_list('fecha', 'bodega__codigo', 'bodega__descripcion', 'genero__codigo', 'genero__descripcion', 
                                                        'edad',  
                                                        'producto__codigo', 'producto__descripcion', 
                                                        'color__codigo', 'color__descripcion', 
                                                        'talla__codigo', 'talla__descripcion', 
                                                        'silueta__codigo', 'silueta__descripcion', 
                                                        'motivo__codigo', 'motivo__descripcion', 'material__codigo','material__descripcion','diseno__codigo','diseno__descripcion','observacion')
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
    paginator = Paginator(ventas_no_realizadas, 20)  # Cambiar el número "10" por la cantidad de elementos que deseas mostrar por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "ventasapp/listar_movimiento.html", {
        "ventas_no_realizadas": page_obj
    })
