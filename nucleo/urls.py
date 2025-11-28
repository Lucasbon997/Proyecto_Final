from django.urls import path
from .views import InicioView, AcercaDeView

app_name = "nucleo"

urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),
    path("about/", AcercaDeView.as_view(), name="acerca_de"),
]
