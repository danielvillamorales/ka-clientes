from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.color import Color

from ..forms import ColorCrearForm, ColorEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def colores(request):
    lista_datos = None
    modelo = "color"
    mensaje = 'Usuario no tiene permiso de ver ' + modelo
    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request,  modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        lista_datos = Color.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_color.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
def crear_color(request):
    titulo = "Color"
    form = ColorCrearForm()
    try:
        if request.method == "POST":
            mensaje_error = existe_registro(Color, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            else:
                form = ColorCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_colores"))
        else:
            context = {
                'form':form,
                'titulo':titulo
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
def editar_color(request, color_id):
    titulo="Color"
    color = Color.objects.get(id=color_id)
    form = ColorEditarForm(instance=color)

    if request.method =='POST':
        print('Actualizando formulario: ', request.POST)
        form=ColorEditarForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_colores"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_color(request, color_id):
    try:
        color = Color.objects.get(id=color_id)
        color.delete()
    except ProtectedError as e:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_colores"))
