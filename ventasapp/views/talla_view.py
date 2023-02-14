from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.talla import Talla

from ..forms import TallaCrearForm, TallaEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def tallas(request):
    lista_datos = None
    modelo = "talla"
    mensaje = 'Usuario no tiene permiso de ver ' + modelo
    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request,  modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        lista_datos = Talla.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_talla.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar
    })

@login_required(login_url='ventasapp:login')
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

@login_required(login_url='ventasapp:login')
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
    try:
        talla = Talla.objects.get(id=talla_id)
        talla.delete()
    except ProtectedError as e:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_tallas"))
