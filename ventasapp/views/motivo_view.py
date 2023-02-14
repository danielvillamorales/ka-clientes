from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.motivo import Motivo

from ..forms import MotivoCrearForm, MotivoEditarForm

from .utils import existe_registro, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar, usuario_puede_listar

@login_required(login_url='ventasapp:login')
def motivos(request):
    lista_datos = None
    mensaje = 'Usuario no tiene permiso de ver motivos'
    puede_adicionar = usuario_puede_adicionar(request,  "motivo")
    puede_editar = usuario_puede_editar(request,  "motivo")
    puede_eliminar = usuario_puede_eliminar(request,  "motivo")
    puede_listar = usuario_puede_listar(request, "motivo")

    if puede_listar:
        lista_datos = Motivo.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_motivo.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
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

@login_required(login_url='ventasapp:login')
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
    try:
        motivo = Motivo.objects.get(id=motivo_id)
        motivo.delete()
    except ProtectedError:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_motivos"))
