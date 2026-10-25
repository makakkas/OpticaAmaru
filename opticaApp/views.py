import random
import string
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from opticaApp.models import *
from opticaApp.forms import *     # trae los formularios y la función rut_valido


def crear_folio():
    # Código de seguimiento al azar: AMR- y 6 letras o números
    letras = string.ascii_uppercase + string.digits
    return "AMR-" + "".join(random.choices(letras, k=6))


# PANTALLAS DEL CLIENTE (no necesitan iniciar sesión) =  Version sin login es mejor wn menos show aunq no lo quiere asi creo lol

def inicio(request):
    return render(request, 'inicio.html')


# HU08: el cliente pide sus lentes.
# Si entra normal (GET) se muestra el formulario vacío.
# Si aprieta "Enviar" (POST) Django revisa los datos con SolicitudForm (mira forms.py) y, si todo está bien, se guarda.
def solicitar(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)   # request.FILES trae el archivo de la receta
        if form.is_valid():
            datos = form.cleaned_data                        # ya revisados y ordenados (el RUT ya viene como 16482915-4)
            estado_inicial = Estado.objects.order_by('orden').first()    # el primer estado: "Recibida"

            if estado_inicial is None:
                form.add_error(None, 'Faltan datos en la base (tipos de lente y estados). Importen base.sql en phpMyAdmin.')
            else:
                # get_or_create: si ya existe un cliente con ese RUT lo usa; si no, lo crea
                cliente, creado = Cliente.objects.get_or_create(
                    rut=datos['rut'],
                    defaults={'nombre': datos['nombre'], 'contacto': datos['contacto'],
                              'telefono': datos['telefono'], 'email': datos['email'], 'acepta_datos': True})
                solicitud = Solicitud(
                    folio=crear_folio(),
                    cliente=cliente,
                    tipo=datos['tipo'],
                    estado=estado_inicial,
                    filtro_azul=datos['filtro_azul'],
                    indicaciones=datos['indicaciones'],
                    fecha_entrega=date.today() + timedelta(days=7),    # estimamos 7 días
                )
                if datos['receta'] and not datos['sin_receta']:
                    solicitud.receta = datos['receta']
                solicitud.save()
                return redirect('solicitud_creada', folio=solicitud.folio)
    else:
        form = SolicitudForm()     # primera vez que entra: formulario vacío

    # Si hubo errores, el mismo "form" vuelve con lo que escribió y con los mensajes de error
    return render(request, 'solicitar.html', {'form': form})


def solicitud_creada(request, folio):
    solicitud = get_object_or_404(Solicitud, folio=folio)
    return render(request, 'solicitud_creada.html', {'solicitud': solicitud})


# HU06: el cliente consulta cómo va su solicitud con su RUT y su código
def consultar_estado(request):
    solicitud = None
    error = ''

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            rut = rut_valido(form.cleaned_data['rut'])
            folio = form.cleaned_data['folio'].strip().upper()
            if rut is not None:
                # Se busca una solicitud que tenga ESE código Y que sea de ESE cliente
                solicitud = Solicitud.objects.filter(folio=folio, cliente__rut=rut).first()
        if solicitud is None:
            # Mismo mensaje si falla el RUT o el código, para no dar pistas
            error = 'No encontramos una solicitud con esos datos. Revisa el RUT y el código.'
    else:
        form = ConsultaForm()

    estados = Estado.objects.order_by('orden')     # los pasos de la línea de tiempo
    return render(request, 'consultar_estado.html', {'form': form, 'solicitud': solicitud, 'error': error, 'estados': estados})


# PANTALLAS DEL PERSONAL
# @login_required = "solo si inició sesión". Si no, lo manda al login del admin (LOGIN_URL en settings.py)


# HU03: cola de solicitudes con indicadores y buscador
@login_required
def lista_solicitudes(request):
    solicitudes = Solicitud.objects.select_related('cliente', 'tipo', 'estado').order_by('-fecha_creacion')

    # Buscador: ?q=algo en la dirección. Q permite decir "esto O esto O esto"
    q = request.GET.get('q', '').strip()
    if q:
        solicitudes = solicitudes.filter(
            Q(folio__icontains=q) | Q(cliente__nombre__icontains=q) | Q(cliente__rut__icontains=q.replace('.', '')))

    # Indicadores de arriba (.count() cuenta cuántas hay)
    todas = Solicitud.objects.all()
    activas = todas.exclude(estado__orden=6).count()                   # 6 = Entregada
    en_taller = todas.filter(estado__orden=3).count()                  # 3 = En taller
    listas = todas.filter(estado__orden=5).count()                     # 5 = Lista para retiro
    con_demora = todas.filter(fecha_entrega__lt=date.today(), estado__orden__lt=5).count()

    return render(request, 'lista_solicitudes.html', {
        'solicitudes': solicitudes, 'q': q,
        'activas': activas, 'en_taller': en_taller, 'listas': listas, 'con_demora': con_demora})


# Detalle de una solicitud. Aquí el personal también cambia el estado.
@login_required
def detalle_solicitud(request, idSolicitud):
    solicitud = get_object_or_404(Solicitud, pk=idSolicitud)

    if request.method == 'POST':
        form = EstadoForm(request.POST, instance=solicitud)   # instance = "edita ESTA solicitud"
        if form.is_valid():
            form.save()
            return redirect('detalle_solicitud', idSolicitud=idSolicitud)
    else:
        form = EstadoForm(instance=solicitud)

    return render(request, 'detalle_solicitud.html', {'solicitud': solicitud, 'form': form})
