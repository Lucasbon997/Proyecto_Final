import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render


from .models import Pagina, Categoria, Compra, Reseña
from .forms import ReseñaFormulario
from cuentas.models import Perfil




class ListaPaginasView(ListView):
    model = Pagina
    template_name = "paginas/lista_paginas.html"
    context_object_name = "paginas"

    def get_queryset(self):
        consulta = super().get_queryset().order_by("-fecha_publicacion")

     
        termino = self.request.GET.get("q")
        if termino:
            consulta = consulta.filter(titulo__icontains=termino)

      
        categoria_id = self.request.GET.get("categoria")
        if categoria_id:
            consulta = consulta.filter(categoria_id=categoria_id)

        return consulta

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["categorias"] = Categoria.objects.all().order_by("nombre")
        contexto["categoria_seleccionada"] = self.request.GET.get("categoria")
        return contexto

class DetallePaginaView(DetailView):
    model = Pagina
    template_name = "paginas/detalle_pagina.html"
    context_object_name = "pagina"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        compra = None
        reseñas = Reseña.objects.filter(producto=self.object)

        reseña_usuario = None
        formulario_reseña = None

        if self.request.user.is_authenticated:
          
            compra = Compra.objects.filter(
                usuario=self.request.user,
                producto=self.object
            ).first()

         
            reseña_usuario = Reseña.objects.filter(
                producto=self.object,
                usuario=self.request.user
            ).first()

            
            if compra and not reseña_usuario:
                formulario_reseña = ReseñaFormulario()

        contexto["compra_usuario"] = compra
        contexto["reseñas"] = reseñas
        contexto["reseña_usuario"] = reseña_usuario
        contexto["formulario_reseña"] = formulario_reseña
        return contexto




class SoloStaffMixin(UserPassesTestMixin):
    """Mixin para permitir solo a usuarios de staff/admin."""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect("nucleo:inicio")

class CrearPaginaView(LoginRequiredMixin, SoloStaffMixin, CreateView):
    model = Pagina
    fields = ["titulo", "subtitulo", "categoria", "precio", "contenido", "imagen"]
    template_name = "paginas/formulario_pagina.html"
    success_url = reverse_lazy("paginas:lista_paginas")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class ActualizarPaginaView(LoginRequiredMixin, SoloStaffMixin, UpdateView):
    model = Pagina
    fields = ["titulo", "subtitulo", "categoria", "precio", "contenido", "imagen"]
    template_name = "paginas/formulario_pagina.html"
    success_url = reverse_lazy("paginas:lista_paginas")

class EliminarPaginaView(LoginRequiredMixin, SoloStaffMixin, DeleteView):
    model = Pagina
    template_name = "paginas/confirmar_eliminar_pagina.html"
    success_url = reverse_lazy("paginas:lista_paginas")

class PreguntasFrecuentesView(TemplateView):
    template_name = "paginas/preguntas_frecuentes.html"


class SoporteView(TemplateView):
    template_name = "paginas/soporte.html"


class GuiaCompraView(TemplateView):
    template_name = "paginas/guia_compra.html"


class BlogInicioView(TemplateView):
    template_name = "paginas/blog_inicio.html"





@login_required
def comprar_producto(request, pk):
    pagina = get_object_or_404(Pagina, pk=pk)
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method != "POST":
        return redirect("paginas:detalle_pagina", pk=pk)

   
    compra_existente = Compra.objects.filter(
        usuario=request.user,
        producto=pagina
    ).first()

    if compra_existente:
       
        if compra_existente.licencia == "TEMP":
            compra_existente.licencia = generar_licencia()
            compra_existente.save()

        messages.info(
            request,
            f"Ya compraste este producto. Tu licencia es: {compra_existente.licencia}"
        )
        return redirect("paginas:detalle_pagina", pk=pk)


    if perfil.saldo < pagina.precio:
        messages.error(request, "No tienes saldo suficiente para comprar este producto.")
        return redirect("paginas:detalle_pagina", pk=pk)
    perfil.saldo -= pagina.precio
    perfil.save()
    licencia = generar_licencia()
    compra = Compra.objects.create(
        usuario=request.user,
        producto=pagina,
        precio_pagado=pagina.precio,
        licencia=licencia,
    )

    messages.success(
        request,
        f"Compra realizada con éxito. Tu licencia es: {compra.licencia}"
    )
    return redirect("paginas:detalle_pagina", pk=pk)



@login_required
@require_POST
def crear_reseña(request, pk):
    pagina = get_object_or_404(Pagina, pk=pk)

    compro = Compra.objects.filter(usuario=request.user, producto=pagina).exists()
    if not compro:
        messages.error(request, "Solo puedes dejar reseña si compraste este producto.")
        return redirect("paginas:detalle_pagina", pk=pk)

    reseña_existente = Reseña.objects.filter(producto=pagina, usuario=request.user).first()
    if reseña_existente:
        messages.info(request, "Ya has dejado una reseña para este producto.")
        return redirect("paginas:detalle_pagina", pk=pk)

    formulario = ReseñaFormulario(request.POST)
    if formulario.is_valid():
        reseña = formulario.save(commit=False)
        reseña.producto = pagina
        reseña.usuario = request.user

        opinion = formulario.cleaned_data["opinion"]
        reseña.me_gusta = (opinion == "like")

        reseña.save()
        messages.success(request, "Tu reseña se ha guardado correctamente.")
    else:
        messages.error(request, "Hay errores en el formulario de reseña.")

    return redirect("paginas:detalle_pagina", pk=pk)


@login_required
def editar_reseña(request, pk):
    reseña = get_object_or_404(Reseña, pk=pk, usuario=request.user)

    if request.method == "POST":
        formulario = ReseñaFormulario(request.POST, instance=reseña)
        if formulario.is_valid():
            opinion = formulario.cleaned_data["opinion"]
            reseña.me_gusta = (opinion == "like")
            reseña = formulario.save(commit=False)
            reseña.save()
            messages.success(request, "Tu reseña fue actualizada correctamente.")
            return redirect("paginas:detalle_pagina", pk=reseña.producto.pk)
        else:
            messages.error(request, "Hay errores en el formulario de reseña.")
    else:
        opinion_inicial = "like" if reseña.me_gusta else "dislike"
        formulario = ReseñaFormulario(
            instance=reseña,
            initial={"opinion": opinion_inicial},
        )

    contexto = {
        "pagina": reseña.producto,
        "formulario_reseña": formulario,
        "reseña": reseña,
        "modo_edicion": True,
    }
    return render(request, "paginas/editar_reseña.html", contexto)





def generar_licencia():
    caracteres = string.ascii_uppercase + string.digits
    while True:
        bloques = ["".join(random.choices(caracteres, k=4)) for _ in range(4)]
        licencia = "-".join(bloques)
        if not Compra.objects.filter(licencia=licencia).exists():
            return licencia




@login_required
def mis_compras(request):
    
    compras = (
        Compra.objects
        .filter(usuario=request.user)
        .select_related("producto")
        .order_by("-fecha_compra")
    )

    contexto = {
        "compras": compras,
    }
    return render(request, "paginas/mis_compras.html", contexto)




