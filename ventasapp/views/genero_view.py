from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.genero import Genero

from ..forms import GeneroCrearForm, GeneroEditarForm

from .utils import existe_registro

def generos(request):
    lista_datos = Genero.objects.all()
    return render(request, "modelos/detalle_genero.html", {
        "lista_datos":lista_datos,
    })

def crear_genero(request):
    titulo = "Géneros"
    form = GeneroCrearForm()
    try:
        if request.method=="POST":
            mensaje_error = existe_registro(Genero, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            
            else:
                form = GeneroCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_generos"))

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

def editar_genero(request, genero_id):
    titulo="Géneros"
    genero = Genero.objects.get(id=genero_id)
    form = GeneroEditarForm(instance=genero)

    if request.method =='POST':

        form=GeneroEditarForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_generos"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_genero(request, genero_id):
    genero = Genero.objects.get(id=genero_id)
    genero.delete()
    return HttpResponseRedirect(reverse("ventasapp:detalle_generos"))