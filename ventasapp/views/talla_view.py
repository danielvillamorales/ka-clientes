from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.talla import Talla

from ..forms import TallaCrearForm, TallaEditarForm

from .utils import existe_registro

def tallas(request):
    lista_datos = Talla.objects.all()
    return render(request, "modelos/detalle_talla.html", {
        "lista_datos":lista_datos,
    })

def crear_talla(request):
    titulo = "Tallas"
    form = TallaCrearForm()

    try:
        if request.method == "POST":
            mensaje_error = existe_registro(Talla, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            
            else:
                form = TallaCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_tallas"))

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

def editar_talla(request, talla_id):
    titulo="Tallas"
    talla = Talla.objects.get(id=talla_id)
    form = TallaEditarForm(instance=talla)

    if request.method =='POST':

        form=TallaEditarForm(request.POST, instance=talla)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_tallas"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_talla(request, talla_id):
    talla = Talla.objects.get(id=talla_id)
    talla.delete()
    return HttpResponseRedirect(reverse("ventasapp:detalle_tallas"))