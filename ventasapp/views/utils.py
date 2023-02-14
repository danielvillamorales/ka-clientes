import xlwt
import pandas as pd
import xlrd
from openpyxl import load_workbook

def existe_registro(instancia, request):
    bodega_existente = instancia.objects.filter(codigo=request.POST['codigo'])
    if bodega_existente:
        return "Ya existe más de un registro con el código indicado \n" + str(bodega_existente[0].codigo) + "-" + str(bodega_existente[0].descripcion)
    else:
        return None

def exportar_modelo(instancia, nombre):
    wb = xlwt.Workbook(encoding='utf-8')
    #ws = wb.add_sheet('nombre') # Nombre del libro

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Codigo', 'Descripcion']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = instancia.objects.all().values_list('codigo','descripcion')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    today    = date.today()
    strToday = today.strftime("%Y-%m-%d")

    nombre = nombre + strToday + ".xls"

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' +nombre+''
    wb.save(response)

    return response

def usuario_puede_listar(request, modelo):
    permisos = request.user.get_all_permissions()
    superusuario = request.user.is_superuser
    puede_listar = ('ventasapp.view_' + modelo in permisos) or (superusuario)

    return puede_listar

def usuario_puede_adicionar(request, modelo):
    permisos = request.user.get_all_permissions()
    superusuario = request.user.is_superuser
    puede_adicionar = ('ventasapp.add_' + modelo in permisos) or (superusuario)

    return puede_adicionar

def usuario_puede_editar(request, modelo):
    permisos = request.user.get_all_permissions()
    superusuario = request.user.is_superuser
    puede_editar = ('ventasapp.change_' + modelo in permisos) or (superusuario)

    return puede_editar

def usuario_puede_eliminar(request, modelo):
    permisos = request.user.get_all_permissions()
    superusuario = request.user.is_superuser
    puede_eliminar = ('ventasapp.delete_' + modelo in permisos) or (superusuario)

    return puede_eliminar
