from django.views.generic import TemplateView
from paginas.models import Pagina
from .models import DestacadoInicio


class InicioView(TemplateView):
    template_name = "nucleo/inicio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["destacados"] = DestacadoInicio.objects.filter(activo=True)[:3]
        contexto["productos_recientes"] = Pagina.objects.order_by("-fecha_publicacion")[:4]
        return contexto


class AcercaDeView(TemplateView):
    template_name = "nucleo/acerca_de.html"
