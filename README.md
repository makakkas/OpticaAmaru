# Óptica Amaru · Front end en Django

Hecho al mismo nivel que **Estacionamientos**: una app (`opticaApp`), vistas con funciones, plantillas con Bootstrap, MySQL de XAMPP y un `base.sql` con datos de ejemplo.

## Cómo partir (XAMPP + phpMyAdmin, como en clases)

1. Encender **Apache** y **MySQL** en XAMPP.
2. En phpMyAdmin: **Nuevo** → nombre `optica_amaru_bd` → **Crear**.
3. En la carpeta del proyecto:
   ```
   pip install django mysqlclient
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. En phpMyAdmin: entrar a `optica_amaru_bd` → **Importar** → elegir `base.sql`.
   (Carga los tipos de lente y los estados, que el formulario necesita, y unos clientes de ejemplo.)
5. `python manage.py runserver` y abrir http://127.0.0.1:8000

Sin XAMPP: en `OpticaAmaru/settings.py` comentan el bloque de MySQL y descomentan el de SQLite. En ese caso, los tipos de lente y los estados se agregan a mano en http://127.0.0.1:8000/admin/ (5 tipos y 6 estados; los nombres están en `base.sql`).

## Qué hay en cada archivo

| Archivo | Para qué sirve | En Estacionamientos era |
|---|---|---|
| `opticaApp/models.py` | 4 tablas: `TipoLente`, `Estado`, `Cliente`, `Solicitud` | `Vehiculo`, `Estacionamiento`, `Ubicacion`, `Utiliza` |
| `opticaApp/views.py` | Una función por pantalla | `views.py` |
| `opticaApp/forms.py` | Los formularios: qué campos tienen y cómo se revisan | `forms.py` (estaba comentado) |
| `OpticaAmaru/urls.py` | Las direcciones de cada pantalla | `urls.py` |
| `opticaApp/admin.py` | Cómo se ven las tablas en `/admin/` | `admin.py` |
| `templates/` | Las páginas HTML. Inicio, solicitar, consultar estado y solicitud enviada son archivos completos (con su `<head>`, menú y pie). Las del personal usan `base.html` | `templates/` |
| `static/css/amaru.css` | Los colores y detalles de Amaru, para no repetirlos en cada HTML | — |
| `base.sql` | Datos de ejemplo | `base.sql` |
| `opticaApp/tests.py` | 16 pruebas automáticas (`python manage.py test`) | estaba vacío |

Lo único nuevo respecto a Estacionamientos:
- **Formularios (`forms.py`)**: cada formulario es una clase y cada campo una línea. En la vista: `form = SolicitudForm(request.POST, request.FILES)`, `form.is_valid()` y `form.cleaned_data`. En el HTML: `{{ form.rut }}` dibuja el campo y `{{ form.rut.errors }}` muestra sus errores. Los métodos `clean_rut` y `clean` hacen las revisiones. Hay tres: `SolicitudForm` y `ConsultaForm` (son `Form`) y `EstadoForm` (es `ModelForm`, sale de la tabla `Solicitud`).
- **`{% csrf_token %}`**: va dentro de todo `<form method="post">`. Django lo exige.
- **`@login_required`**: encima de las vistas del personal. Si no iniciaron sesión, las manda al login del admin. Se entra con el usuario que crearon con `createsuperuser`.
- **`templates/base.html`**: solo lo usan las pantallas del personal (`{% extends 'base.html' %}`).
- **Carpeta `static/`**: el logo, la foto y el CSS (`{% load static %}` y `{% static 'css/amaru.css' %}`).

## Pantallas

| Pantalla | Dirección | Historia |
|---|---|---|
| Inicio | `/` | — |
| Solicitar lentes | `/solicitar/` | HU08 |
| Consultar estado (RUT + código) | `/estado/` | HU06 |
| Panel de solicitudes (personal) | `/panel/` | HU03 |
| Detalle y cambio de estado (personal) | `/panel/<número>/` | HU03 |

## Lo que falta (siguiente paso del cronograma)

Reserva de horas (HU11), pantallas de clientes y consentimiento (HU10), búsqueda con historial y recetas (HU02, HU04, HU05), postventa (HU07) y aceptación o firma (HU09). También quedan para después, porque son más avanzados: historial de cambios de estado, avisos por WhatsApp o correo, y proteger las recetas (hoy quedan en `media/` y se abren con su dirección).
