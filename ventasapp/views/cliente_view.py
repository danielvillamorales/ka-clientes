import openpyxl
from django.shortcuts import get_object_or_404,render, redirect
from django.views.decorators.csrf import csrf_protect
from ventasapp.models.clientes import Cliente , VentasClientesPsv
from ventasapp.models.bodega import Bodega
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User,Permission,Group
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
import xlwt




def import_cliente(request):
    if request.user.has_perm('ventasapp.importar_clientes'):
        try:
            # Obtenga el archivo de Excel del formulario
            excel_file = request.FILES['excel_file']
            # Importe el archivo de Excel
            wb = openpyxl.load_workbook(excel_file)
            # Obtenga la hoja de trabajo activa
            sheet = wb.get_sheet_by_name("clientes")

            # Crear una lista de objetos Cliente
            clientes = []
            contador = 1
            for r in sheet.rows:
                nombre = r[0].value
                cedula = r[1].value
                telefono = r[3].value
                #print(f'{nombre} - {cedula} - {telefono} - {r[2].value}')
                try:
                    almacen = Bodega.objects.get(codigo=str(r[2].value).upper())
                    #print(almacen)
                    cliente = Cliente(
                        nombre=nombre,
                        cedula=cedula,
                        bodega=almacen,
                        telefono=telefono,
                        fecha_subida=datetime.now(),
                    )
                    clientes.append(cliente)
                except Exception as e:
                    messages.error(request, f'Error en la fila: {contador} No existe la bodega')
                    return render(request, 'cliente/importar.html')
                contador += 1
            # Guardar los objetos Cliente en la base de datos
            Cliente.objects.bulk_create(clientes)
            messages.success(request, f'Clientes subido correctamente')
        except Exception as e:
            messages.error(request, f'Error al subir clientes: (estructura del archivo o nombre de la hoja incorrectos) {e}')
    else:
        messages.warning(request, 'No tiene permisos para subir clientes')
    return render(request, 'cliente/importar.html')

@login_required(login_url='ventasapp:login')    
def importacion(request):
    if request.method == 'POST':
        import_cliente(request)
    return render(request, 'cliente/importar.html')


@login_required(login_url='ventasapp:login')
def listado_clientes(request):
    user = get_object_or_404(User, username = request.user)
    print(user.usuario_bodega.bodega.codigo)
    if request.method == 'POST':
        saveObservationClient(request)
    clientes = Cliente.objects.filter(bodega__codigo=user.usuario_bodega.bodega.codigo).filter(observaciones__isnull=True)
    paginator = Paginator(clientes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cliente/detalle_cliente.html', {"clientes": page_obj})


def saveObservationClient(request):
        cliente = get_object_or_404(Cliente, id = request.POST.get('idform'))
        cliente.observaciones = request.POST.get('observaciones')
        cliente.fecha_llamada = datetime.now()
        cliente.save()
        messages.success(request, f'Cliente actualizado correctamente')


def consultar_cliente(request):
    if request.method == 'GET':
        cedula = request.GET.get('cedula')
        clientes = Cliente.objects.filter(cedula=cedula).filter(observaciones__isnull=False)
        return render(request, 'cliente/consultar_cliente.html', {"clientes": clientes})
    return render(request, 'cliente/consultar_cliente.html')

def exportar_clientes(request):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Clientes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nombre', 'Cedula', 'Bodega', 'Telefono', 'Fecha Subida', 'Observaciones', 'Fecha Llamada', 'ventas', 'valor_venta']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Cliente.objects.filter(observaciones__isnull=False).values_list('nombre', 'cedula', 'bodega__descripcion', 'telefono', 'fecha_subida', 'observaciones', 'fecha_llamada')
    cedulas = [row[1] for row in rows]
    anos_llamada = list(set([row[6].year for row in rows]))
    ventas_clientes = VentasClientesPsv.objects.using('logistica_db').filter(ms_nit__in=cedulas, anio__in=anos_llamada)
# Crear un diccionario para mapear ventas por cliente y año
    ventas_dict = {}
    for venta in ventas_clientes:
        key = (venta.ms_nit, venta.anio)
        if key not in ventas_dict:
            ventas_dict[key] = {
                'ventas': [],
                'total_vendido': 0,
            }
        ventas_dict[key]['ventas'].append(str(venta))
        ventas_dict[key]['total_vendido'] += venta.vendido or 0

    # Procesar los datos y escribir en el archivo
    for row_num, row in enumerate(rows, start=1):
        cliente_compra = ventas_dict.get((row[1], str(row[6].year)), {})
        #print(cliente_compra)
        for col_num, value in enumerate(row):
            if isinstance(value, datetime):
                formatted_date = value.strftime('%Y-%m-%d %H:%M:%S')
                ws.write(row_num, col_num, formatted_date, font_style)
            else:
                ws.write(row_num, col_num, value, font_style)
        if len(cliente_compra)> 0:
            ws.write(row_num, 7, '\n'.join(map(str, cliente_compra['ventas'])), font_style)
            ws.write(row_num, 8, cliente_compra['total_vendido'], font_style)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=clientes.xls'
    # Guardar el contenido del libro de trabajo en un búfer BytesIO
    output = BytesIO()
    wb.save(output)
    
    # Configurar la posición del búfer al principio
    output.seek(0)
    
    # Configurar el contenido del búfer como contenido de la respuesta
    response.write(output.getvalue())
    
    return response
