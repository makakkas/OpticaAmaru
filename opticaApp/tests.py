##ESTO ADMITO QUE OCUPE IA, NO EN TODO, MAS QUE NADA PARA ENTENDERLO XQ NI PUTA IDEA PERO ERA MUCHO Y ME AYUDE CON LA IA QLA YIAAA OE Q ME CAE MAL EL YOKO, HOLA

import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from opticaApp.models import *
from opticaApp.views import rut_valido



class RutTests(TestCase):
    def test_rut_bueno(self):
        self.assertEqual(rut_valido('16.482.915-4'), '16482915-4')
        self.assertEqual(rut_valido('12345678-5'), '12345678-5')

    def test_rut_malo(self):                          
        self.assertIsNone(rut_valido('16.482.915-3')) 
        self.assertIsNone(rut_valido(''))
        self.assertIsNone(rut_valido('abc'))


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BaseTests(TestCase):
    def setUp(self):
        self.tipo = TipoLente.objects.create(nombre='Lentes de lectura')
        for numero, nombre in enumerate(['Recibida', 'En revisión', 'En taller', 'Control de calidad',
                                         'Lista para retiro', 'Entregada'], start=1):
            Estado.objects.create(nombre=nombre, orden=numero)

    def datos(self, **cambios):
        d = {'rut': '16.482.915-4', 'nombre': 'Carlos Rojas', 'contacto': 'WhatsApp',
             'telefono': '+56 9 5551 0101', 'tipo': self.tipo.idTipoLente, 'acepta_datos': 'on',
             'receta': SimpleUploadedFile('receta.png', b'contenido de prueba', content_type='image/png')}
        d.update(cambios)
        return d


class SolicitarTests(BaseTests):
    def test_solicitud_correcta(self):            
        respuesta = self.client.post(reverse('solicitar'), self.datos())
        solicitud = Solicitud.objects.get()
        self.assertRedirects(respuesta, reverse('solicitud_creada', args=[solicitud.folio]))
        self.assertEqual(solicitud.cliente.rut, '16482915-4')
        self.assertEqual(solicitud.estado.nombre, 'Recibida')

    def test_rut_invalido_no_guarda_nada(self):     
        self.client.post(reverse('solicitar'), self.datos(rut='16.482.915-3'))
        self.assertEqual(Cliente.objects.count(), 0)
        self.assertEqual(Solicitud.objects.count(), 0)

    def test_sin_autorizacion_no_se_envia(self):  
        datos = self.datos()
        del datos['acepta_datos']
        self.client.post(reverse('solicitar'), datos)
        self.assertEqual(Solicitud.objects.count(), 0)

    def test_el_error_se_muestra_y_no_borra_lo_escrito(self):
        r = self.client.post(reverse('solicitar'), self.datos(rut='16.482.915-3'))
        self.assertContains(r, 'El RUT no es válido')      # el mensaje sale en la página
        self.assertContains(r, 'Carlos Rojas')              # y el nombre sigue escrito en el formulario

    def test_prefiere_correo_pero_no_lo_escribe(self):
        r = self.client.post(reverse('solicitar'), self.datos(contacto='Correo'))
        self.assertContains(r, 'necesitamos tu correo')
        self.assertEqual(Solicitud.objects.count(), 0)

    def test_receta_con_formato_malo(self):
        malo = SimpleUploadedFile('virus.exe', b'MZ...')
        self.client.post(reverse('solicitar'), self.datos(receta=malo))
        self.assertEqual(Solicitud.objects.count(), 0)

    def test_sin_receta_pero_marcando_la_opcion(self):
        datos = self.datos(sin_receta='on')
        del datos['receta']
        self.client.post(reverse('solicitar'), datos)
        self.assertEqual(Solicitud.objects.count(), 1)


class ConsultaTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('solicitar'), self.datos())
        self.solicitud = Solicitud.objects.get()

    def test_consulta_correcta(self):                 # HU06
        r = self.client.post(reverse('consultar_estado'),
                             {'rut': '16.482.915-4', 'folio': self.solicitud.folio.lower()})
        self.assertContains(r, 'Recibida')

    def test_rut_ajeno_no_ve_la_solicitud(self):      # P07
        Cliente.objects.create(rut='12345678-5', nombre='Otra Persona')
        r = self.client.post(reverse('consultar_estado'),
                             {'rut': '12.345.678-5', 'folio': self.solicitud.folio})
        self.assertContains(r, 'No encontramos')
        self.assertNotContains(r, 'Carlos')


class PersonalTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('solicitar'), self.datos())
        self.solicitud = Solicitud.objects.get()
        User.objects.create_user('personal', password='clave-de-prueba-123')

    def test_panel_pide_iniciar_sesion(self):
        r = self.client.get(reverse('lista_solicitudes'))
        self.assertEqual(r.status_code, 302)           # 302 = lo redirige al login

    def test_panel_con_sesion(self):
        self.client.login(username='personal', password='clave-de-prueba-123')
        r = self.client.get(reverse('lista_solicitudes'))
        self.assertContains(r, self.solicitud.folio)
        self.assertContains(r, '16.***.915-4')         # el RUT sale tapado
        self.assertNotContains(r, '16482915-4')

    def test_buscar_por_rut(self):
        self.client.login(username='personal', password='clave-de-prueba-123')
        self.assertContains(self.client.get(reverse('lista_solicitudes'), {'q': '16.482.915-4'}),
                            self.solicitud.folio)
        self.assertNotContains(self.client.get(reverse('lista_solicitudes'), {'q': '99999999'}),
                               self.solicitud.folio)

    def test_cambiar_estado(self):                    # HU03
        self.client.login(username='personal', password='clave-de-prueba-123')
        en_taller = Estado.objects.get(orden=3)
        self.client.post(reverse('detalle_solicitud', args=[self.solicitud.idSolicitud]),
                         {'estado': en_taller.idEstado})
        self.solicitud.refresh_from_db()
        self.assertEqual(self.solicitud.estado.nombre, 'En taller')


class PaginasTests(TestCase):
    def test_paginas_publicas(self):
        for nombre in ('inicio', 'solicitar', 'consultar_estado'):
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200, nombre)
