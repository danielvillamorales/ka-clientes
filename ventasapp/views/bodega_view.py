from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models.bodega import Bodega

from ..forms import BodegaCrearForm, BodegaEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def bodegas(request):
    lista_datos = None
    mensaje = 'Usuario no tiene permiso de ver bodegas'
    puede_adicionar = usuario_puede_adicionar(request,  "bodega")
    puede_editar = usuario_puede_editar(request,  "bodega")
    puede_eliminar = usuario_puede_eliminar(request,  "bodega")
    puede_listar = usuario_puede_listar(request, "bodega")

    if puede_listar:
        lista_datos = Bodega.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_bodega.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
def crear_bodega(request):
    titulo = "Bodega"
    form = BodegaCrearForm()
    try:
        if request.method=="POST":
            mensaje_error = existe_registro(Bodega, request)

            if mensaje_error:
                context = {
                    'form':form,
                    'titulo':titulo,
                    'mensaje_error':mensaje_error
                }
            
            else:
                form = BodegaCrearForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse("ventasapp:detalle_bodegas"))

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
def editar_bodega(request, bodega_id):
    titulo="Bodega"
    bodega = Bodega.objects.get(id=bodega_id)
    form = BodegaEditarForm(instance=bodega)

    if request.method =='POST':
        form=BodegaEditarForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("ventasapp:detalle_bodegas"))
    context = {'form': form, 'titulo': titulo}
    return render(request, "modelos/editar.html", context)

def eliminar_bodega(request, bodega_id):
    try:
        bodega = Bodega.objects.get(id=bodega_id)
        bodega.delete()
    except ProtectedError as e:
        pass

    return HttpResponseRedirect(reverse("ventasapp:detalle_bodegas"))
