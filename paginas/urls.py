from django.urls import path
from .views import (
    ListaPaginasView,
    DetallePaginaView,
    CrearPaginaView,
    ActualizarPaginaView,
    EliminarPaginaView,
    comprar_producto,
    crear_reseña,
    editar_reseña,
    PreguntasFrecuentesView,
    SoporteView,
    GuiaCompraView,
    BlogInicioView,
    mis_compras,
)

app_name = "paginas"

urlpatterns = [
    path("", BlogInicioView.as_view(), name="blog_inicio"),
    path("productos/", ListaPaginasView.as_view(), name="lista_paginas"),
    path("<int:pk>/", DetallePaginaView.as_view(), name="detalle_pagina"),
    path("crear/", CrearPaginaView.as_view(), name="crear_pagina"),
    path("<int:pk>/editar/", ActualizarPaginaView.as_view(), name="editar_pagina"),
    path("<int:pk>/eliminar/", EliminarPaginaView.as_view(), name="eliminar_pagina"),
    path("<int:pk>/comprar/", comprar_producto, name="comprar_producto"),
    path("<int:pk>/reseña/", crear_reseña, name="crear_reseña"),
    path("reseñas/<int:pk>/editar/", editar_reseña, name="editar_reseña"),
    path("faq/", PreguntasFrecuentesView.as_view(), name="faq"),
    path("soporte/", SoporteView.as_view(), name="soporte"),
    path("guia-compra/", GuiaCompraView.as_view(), name="guia_compra"),
    path("mis-compras/", mis_compras, name="mis_compras"),
]

