from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def crear_grupos_por_defecto(sender, **kwargs):

    if sender.name != "cuentas":
        return
    grupo_staff, _ = Group.objects.get_or_create(name="Staff")
    permisos_staff = Permission.objects.all()
    grupo_staff.permissions.set(permisos_staff)

    grupo_soporte, _ = Group.objects.get_or_create(name="Soporte")
    permisos_soporte = Permission.objects.filter(codename__startswith="view_")
    grupo_soporte.permissions.set(permisos_soporte)
    grupo_moderadores, _ = Group.objects.get_or_create(name="Moderadores")
    permisos_moderadores = Permission.objects.filter(
        content_type__app_label__in=["paginas", "mensajeria"]
    )
    grupo_moderadores.permissions.set(permisos_moderadores)
