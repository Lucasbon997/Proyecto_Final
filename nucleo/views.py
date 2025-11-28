from django.views.generic import TemplateView
from paginas.models import Pagina
from .models import DestacadoInicio


class InicioView(TemplateView):
    template_name = "nucleo/inicio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        # Hasta 3 tarjetas activas
        contexto["destacados"] = DestacadoInicio.objects.filter(activo=True)[:3]
        # (Opcional) últimos productos para mostrar abajo, si querés
        contexto["productos_recientes"] = Pagina.objects.order_by("-fecha_publicacion")[:4]
        return contexto


class AcercaDeView(TemplateView): # CBV 2
    template_name = "nucleo/acerca_de.html"
