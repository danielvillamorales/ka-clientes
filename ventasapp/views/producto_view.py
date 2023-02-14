from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.producto import Producto

from ..forms import ProductoCrearForm, ProductoEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def productos(request):
    lista_datos = None
    modelo = "producto"
    mensaje = 'Usuario no tiene permiso de ver ' + modelo
    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request,  modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        lista_datos = Producto.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_producto.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
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

@login_required(login_url='ventasapp:login')
def editar_producto(request, producto_id):
    titulo="Productos"
    producto = Producto.objects.get(id=producto_id)
    form = ProductoEditarForm(instance=producto)

    if request.method =='POST':

        form=ProductoEditarForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_productos"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.delete()
    except ProtectedError as e:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_productos"))
