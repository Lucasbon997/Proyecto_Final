from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import Perfil, TarjetaRegalo
from .forms import (
    RegistroFormulario,
    PerfilFormulario,
    UsuarioFormulario,
    RecargaTarjetaRegaloFormulario,
    RecargaTarjetaFormulario,
)


def registrarse(request):
    if request.method == "POST":
        formulario = RegistroFormulario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            Perfil.objects.create(usuario=usuario)
            login(request, usuario)
            return redirect("nucleo:inicio")
    else:
        formulario = RegistroFormulario()
    return render(request, "cuentas/registrarse.html", {"formulario": formulario})


def ingresar(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect("nucleo:inicio")
    else:
        formulario = AuthenticationForm(request)
    return render(request, "cuentas/ingresar.html", {"formulario": formulario})


@login_required
def salir(request):
    logout(request)
    return redirect("nucleo:inicio")


@login_required
def perfil(request):
    perfil_obj, _ = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, "cuentas/perfil.html", {"perfil": perfil_obj})


@login_required
def editar_perfil(request):
    perfil_obj, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form_usuario = UsuarioFormulario(request.POST, instance=request.user)
        form_perfil = PerfilFormulario(request.POST, request.FILES, instance=perfil_obj)
        if form_usuario.is_valid() and form_perfil.is_valid():
            form_usuario.save()
            form_perfil.save()
            return redirect("cuentas:perfil")
    else:
        form_usuario = UsuarioFormulario(instance=request.user)
        form_perfil = PerfilFormulario(instance=perfil_obj)

    contexto = {
        "form_usuario": form_usuario,
        "form_perfil": form_perfil,
    }
    return render(request, "cuentas/editar_perfil.html", contexto)


@login_required
def cambiar_password(request):
    if request.method == "POST":
        formulario = PasswordChangeForm(user=request.user, data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            update_session_auth_hash(request, usuario)
            return redirect("cuentas:perfil")
    else:
        formulario = PasswordChangeForm(user=request.user)
    return render(request, "cuentas/cambiar_password.html", {"formulario": formulario})


@login_required
def recargar_saldo_tarjeta_regalo(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        formulario = RecargaTarjetaRegaloFormulario(request.POST)
        if formulario.is_valid():
            codigo = formulario.cleaned_data["codigo"]
            try:
                tarjeta = TarjetaRegalo.objects.get(codigo=codigo)
            except TarjetaRegalo.DoesNotExist:
                messages.error(request, "El código ingresado no es válido.")
                return redirect("cuentas:recargar_saldo_regalo")

            if tarjeta.usado:
                messages.error(request, "Esta tarjeta de regalo ya fue utilizada.")
                return redirect("cuentas:recargar_saldo_regalo")

            perfil.saldo += tarjeta.monto
            perfil.save()

            tarjeta.usado = True
            tarjeta.usado_por = request.user
            tarjeta.fecha_uso = timezone.now()
            tarjeta.save()

            messages.success(request, f"Se han acreditado ${tarjeta.monto} a tu saldo.")
            return redirect("cuentas:perfil")
    else:
        formulario = RecargaTarjetaRegaloFormulario()

    contexto = {
        "formulario": formulario,
        "perfil": perfil,
    }
    return render(request, "cuentas/recargar_saldo_regalo.html", contexto)



@login_required
def recargar_saldo_tarjeta(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        formulario = RecargaTarjetaFormulario(request.POST)
        if formulario.is_valid():
            monto = formulario.cleaned_data["monto"]

            perfil.saldo = perfil.saldo + monto
            perfil.save()

            messages.success(
                request,
                f"Se han acreditado ${monto} a tu saldo (simulación de pago)."
            )
            return redirect("cuentas:perfil")
        else:
            messages.error(request, "Hay errores en el formulario. Revisá los datos ingresados.")
    else:
        formulario = RecargaTarjetaFormulario()

    contexto = {
        "formulario": formulario,
        "perfil": perfil,
    }
    return render(request, "cuentas/recargar_saldo_tarjeta.html", contexto)

