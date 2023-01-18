import xlwt

def existe_registro(instancia, request):
    bodega_existente = instancia.objects.filter(codigo=request.POST['codigo'], descripcion=request.POST['descripcion'])
    if bodega_existente:
        return "Ya existe más de un registro con esa información \n" + str(request.POST['codigo']) + "-" + str(request.POST['descripcion'])
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


