from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.color import Color

from ..forms import ColorCrearForm, ColorEditarForm

from .utils import existe_registro

def colores(request):
    lista_datos = Color.objects.all()
    return render(request, "modelos/detalle_color.html", {
        "lista_datos":lista_datos,
    })

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
    color = Color.objects.get(id=color_id)
    color.delete()
    return HttpResponseRedirect(reverse("ventasapp:detalle_colores"))