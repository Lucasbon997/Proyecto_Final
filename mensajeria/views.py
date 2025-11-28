from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .models import SolicitudAmistad, Amistad, ChatMensaje
# Si no lo tenés arriba, asegurate de importar Mensaje y MensajeFormulario:
# from .models import Mensaje
# from .forms import MensajeFormulario


@login_required
def bandeja_entrada(request):
    mensajes = Mensaje.objects.filter(destinatario=request.user).order_by("-fecha_envio")
    return render(request, "mensajeria/bandeja_entrada.html", {"mensajes": mensajes})


@login_required
def detalle_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk, destinatario=request.user)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return render(request, "mensajeria/detalle_mensaje.html", {"mensaje": mensaje})


@login_required
def nuevo_mensaje(request):
    if request.method == "POST":
        formulario = MensajeFormulario(request.POST)
        if formulario.is_valid():
            mensaje = formulario.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect("mensajeria:bandeja_entrada")
    else:
        formulario = MensajeFormulario()
    return render(request, "mensajeria/nuevo_mensaje.html", {"formulario": formulario})


def obtener_amigos(usuario):
    """
    Devuelve un queryset de usuarios que son amigos del usuario dado.
    Como al aceptar una solicitud creamos dos filas (A->B y B->A),
    alcanza con mirar las filas donde 'usuario' es el dueño de la amistad.
    Así evitamos usar union() + distinct(), que dan problemas en SQLite.
    """
    amigos_ids = Amistad.objects.filter(usuario=usuario).values_list("amigo_id", flat=True)
    return User.objects.filter(id__in=amigos_ids)


@login_required
def lista_amigos(request):
    amigos = obtener_amigos(request.user)
    solicitudes_recibidas = SolicitudAmistad.objects.filter(
        para_usuario=request.user,
        estado="pendiente",
    )
    solicitudes_enviadas = SolicitudAmistad.objects.filter(
        de_usuario=request.user,
        estado="pendiente",
    )

    contexto = {
        "amigos": amigos,
        "solicitudes_recibidas": solicitudes_recibidas,
        "solicitudes_enviadas": solicitudes_enviadas,
    }
    return render(request, "mensajeria/lista_amigos.html", contexto)


@login_required
def enviar_solicitud_amistad(request, usuario_id):
    objetivo = get_object_or_404(User, pk=usuario_id)

    if objetivo == request.user:
        messages.error(request, "No puedes enviarte una solicitud a ti mismo.")
        return redirect("mensajeria:lista_amigos")

    # Ya son amigos
    ya_son_amigos = Amistad.objects.filter(usuario=request.user, amigo=objetivo).exists()
    if ya_son_amigos:
        messages.info(request, "Esta persona ya es tu amiga.")
        return redirect("mensajeria:lista_amigos")

    # Ya existe una solicitud pendiente?
    ya_hay_solicitud = SolicitudAmistad.objects.filter(
        de_usuario=request.user,
        para_usuario=objetivo,
        estado="pendiente",
    ).exists()

    if ya_hay_solicitud:
        messages.info(request, "Ya enviaste una solicitud a esta persona.")
        return redirect("mensajeria:lista_amigos")

    SolicitudAmistad.objects.create(
        de_usuario=request.user,
        para_usuario=objetivo,
        estado="pendiente",
    )
    messages.success(request, "Solicitud de amistad enviada.")
    return redirect("mensajeria:lista_amigos")


@login_required
def responder_solicitud_amistad(request, solicitud_id, accion):
    solicitud = get_object_or_404(SolicitudAmistad, pk=solicitud_id, para_usuario=request.user)

    if accion == "aceptar":
        solicitud.estado = "aceptada"
        solicitud.save()

        # Crear relación de amistad en ambos sentidos
        Amistad.objects.get_or_create(usuario=request.user, amigo=solicitud.de_usuario)
        Amistad.objects.get_or_create(usuario=solicitud.de_usuario, amigo=request.user)

        messages.success(request, "Solicitud de amistad aceptada.")
    elif accion == "rechazar":
        solicitud.estado = "rechazada"
        solicitud.save()
        messages.info(request, "Solicitud de amistad rechazada.")
    else:
        messages.error(request, "Acción inválida.")

    return redirect("mensajeria:lista_amigos")


@login_required
def buscar_usuarios(request):
    query = request.GET.get("q", "")
    resultados = []

    if query:
        resultados = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(pk=request.user.pk)

    amigos = obtener_amigos(request.user)
    amigos_ids = set(amigos.values_list("id", flat=True))

    solicitudes_enviadas = SolicitudAmistad.objects.filter(
        de_usuario=request.user,
        estado="pendiente",
    ).values_list("para_usuario_id", flat=True)

    solicitudes_recibidas = SolicitudAmistad.objects.filter(
        para_usuario=request.user,
        estado="pendiente",
    ).values_list("de_usuario_id", flat=True)

    contexto = {
        "query": query,
        "resultados": resultados,
        "amigos_ids": amigos_ids,
        "solicitudes_enviadas_ids": set(solicitudes_enviadas),
        "solicitudes_recibidas_ids": set(solicitudes_recibidas),
    }
    return render(request, "mensajeria/buscar_usuarios.html", contexto)


@login_required
def chat_con_amigo(request, amigo_id):
    amigo = get_object_or_404(User, pk=amigo_id)

    # Verificar que sean amigos
    son_amigos = Amistad.objects.filter(usuario=request.user, amigo=amigo).exists()
    if not son_amigos:
        messages.error(request, "Solo puedes chatear con usuarios que tengas como amigos.")
        return redirect("mensajeria:lista_amigos")

    # Mensajes entre ambos, en ambas direcciones
    mensajes = ChatMensaje.objects.filter(
        Q(de_usuario=request.user, para_usuario=amigo) |
        Q(de_usuario=amigo, para_usuario=request.user)
    ).order_by("fecha_envio")

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            ChatMensaje.objects.create(
                de_usuario=request.user,
                para_usuario=amigo,
                texto=texto,
            )
            return redirect("mensajeria:chat_con_amigo", amigo_id=amigo.id)

    contexto = {
        "amigo": amigo,
        "mensajes": mensajes,
    }
    return render(request, "mensajeria/chat.html", contexto)

