from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError

from ..models.genero import Genero

from ..forms import GeneroCrearForm, GeneroEditarForm

from .utils import existe_registro, usuario_puede_listar, usuario_puede_adicionar, usuario_puede_editar, usuario_puede_eliminar

@login_required(login_url='ventasapp:login')
def generos(request):
    lista_datos = None
    modelo = "genero"
    mensaje = 'Usuario no tiene permiso de ver ' + modelo
    puede_adicionar = usuario_puede_adicionar(request,  modelo)
    puede_editar = usuario_puede_editar(request,  modelo)
    puede_eliminar = usuario_puede_eliminar(request,  modelo)
    puede_listar = usuario_puede_listar(request, modelo)

    if puede_listar:
        lista_datos = Genero.objects.all().order_by('descripcion')
        mensaje = ''

    return render(request, "modelos/detalle_genero.html", {
        "lista_datos":lista_datos,
        "mensaje": mensaje,
        "puede_adicionar": puede_adicionar,
        "puede_editar": puede_editar,
        "puede_eliminar": puede_eliminar,
    })

@login_required(login_url='ventasapp:login')
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

@login_required(login_url='ventasapp:login')
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
    try:
        genero = Genero.objects.get(id=genero_id)
        genero.delete()
    except ProtectedError as e:
        pass
    return HttpResponseRedirect(reverse("ventasapp:detalle_generos"))
