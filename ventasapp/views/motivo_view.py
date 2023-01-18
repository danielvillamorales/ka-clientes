from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.motivo import Motivo

from ..forms import MotivoCrearForm, MotivoEditarForm

from .utils import existe_registro

def motivos(request):
    lista_datos = Motivo.objects.all()
    return render(request, "modelos/detalle_motivo.html", {
        "lista_datos":lista_datos,
    })

def crear_motivo(request):
    titulo = "Motivos"
    form = MotivoCrearForm()

    try:
        if request.method == "POST":
            mensaje_error = existe_registro(Motivo, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            else:
                form = MotivoCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_motivos"))
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

def editar_motivo(request, motivo_id):
    titulo="Motivos"
    motivo = Motivo.objects.get(id=motivo_id)
    form = MotivoEditarForm(instance=motivo)

    if request.method =='POST':

        form=MotivoEditarForm(request.POST, instance=motivo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_motivos"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_motivo(request, motivo_id):
    motivo = Motivo.objects.get(id=motivo_id)
    motivo.delete()
    return HttpResponseRedirect(reverse("ventasapp:detalle_motivos"))