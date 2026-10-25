from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from opticaApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Cliente (no necesita iniciar sesión, o yo creo q es lo mejor xq si no el meo show xdxd)
    path('', inicio, name='inicio'),
    path('solicitar/', solicitar, name='solicitar'),                                     # HU08
    path('solicitar/listo/<str:folio>/', solicitud_creada, name='solicitud_creada'),
    path('estado/', consultar_estado, name='consultar_estado'),                          # HU06

    # Personal (pide iniciar sesión)
    path('panel/', lista_solicitudes, name='lista_solicitudes'),                         # HU03
    path('panel/<int:idSolicitud>/', detalle_solicitud, name='detalle_solicitud'),
]

# Esto permite abrir las recetas subidas mientras se trabaja en el computador, O algo asi me explico el gepeto
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
