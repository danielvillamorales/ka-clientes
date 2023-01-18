from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.producto import Producto

from ..forms import ProductoCrearForm, ProductoEditarForm

from .utils import existe_registro

def productos(request):
    lista_datos = Producto.objects.all()
    return render(request, "modelos/detalle_producto.html", {
        "lista_datos":lista_datos,
    })

def crear_producto(request):
    titulo = "Productos"
    form = ProductoCrearForm()

    try:
        if request.method == "POST":
            mensaje_error = existe_registro(Producto, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            else:
                form = ProductoCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_productos"))
        else:
            context = {
                'form':form,
                'titulo':titulo,
            }
        return render(request, "modelos/crear.html", context)
    except Exception as exception_err:
        context = {
                'form':form,
                'titulo':titulo,
                'mensaje_error': str(exception_err)
                }
        return render(request, "modelos/crear.html", context)

def editar_producto(request, producto_id):
    titulo="Productos"
    producto = Producto.objects.get(id=producto_id)
    form = ProductoEditarForm(instance=producto)

    if request.method =='POST':

        form=ProductoEditarForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            #return redirect('agendar_cita')
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return HttpResponseRedirect(reverse("ventasapp:detalle_productos"))
