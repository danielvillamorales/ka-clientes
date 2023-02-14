from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.silueta import Silueta

from ..forms import SiluetaCrearForm, SiluetaEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def siluetas(request):
    lista_datos = None
    modelo = "silueta"
    mensaje = 'Usuario no tiene permiso de ver ' + modelo
    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request,  modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        lista_datos = Silueta.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_silueta.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
def crear_silueta(request):
    titulo = "Siluetas"
    form = SiluetaCrearForm()

    try:
        if request.method == "POST":
            mensaje_error = existe_registro(Silueta, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            else:
                form = SiluetaCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_siluetas"))

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
def editar_silueta(request, silueta_id):
    titulo="Siluetas"
    instancia = Silueta.objects.get(id=silueta_id)
    form = SiluetaEditarForm(instance=instancia)

    if request.method =='POST':

        form=SiluetaEditarForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_siluetas"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_silueta(request, silueta_id):
    try:
        silueta = Silueta.objects.get(id=silueta_id)
        silueta.delete()
    except ProtectedError as e:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_siluetas"))
