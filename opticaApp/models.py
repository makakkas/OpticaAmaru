from django.db import models



class TipoLente(models.Model):
    idTipoLente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)      # Ej: "Lentes de lectura", "Multifocales"

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)       # Ej: "Recibida", "En taller", "Lista para retiro" y vieja qla te odio yiaa
    orden = models.IntegerField()                  # 1, 2, 3... sirve para dibujar la línea de tiempo

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10, unique=True)   
    nombre = models.CharField(max_length=120)
    contacto = models.CharField(max_length=20)             # WhatsApp, Llamada o Correo, esta wea en realidad es algo por estar nma porq nose si vamos a trabajar con el wp de la tia
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    # El cliente tiene que aceptar que usemos sus datos (incluye su receta, que es un dato de salud)
    acepta_datos = models.BooleanField(default=False)

    def rut_oculto(self):
        # Para las tablas del personal: 16482915-4 se muestra como 16.***.915-4 mas que nd para recalcar las weas q pusimos de seguridad y leyes, el tema de los datos personales y weas xd
        return self.rut[:2] + ".***." + self.rut[-5:]

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


class Solicitud(models.Model):
    idSolicitud = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=12, unique=True)   # el código de seguimiento, ej: AMR-4F7K2Q
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='solicitudes')
    tipo = models.ForeignKey(TipoLente, on_delete=models.CASCADE, related_name='solicitudes')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='solicitudes')
    # blank=True: puede quedar vacío (por ejemplo si el cliente no tiene receta)
    receta = models.FileField(upload_to='recetas/', blank=True)
    filtro_azul = models.BooleanField(default=False)
    indicaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)   # pa que se cree solo la fecha y hora cuando se crea la solicitud
    fecha_entrega = models.DateField(null=True, blank=True)   

    def __str__(self):
        return f"{self.folio} - {self.cliente.nombre}"
