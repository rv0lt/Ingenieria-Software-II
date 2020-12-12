from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import hashers
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher as psph


class Marca(models.Model):
    marca = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.marca


class Modelo(models.Model):
    marca_fk = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)

    def __str__(self):
        return str(Marca.objects.get(id=self.marca_fk.id)) + self.modelo


class Cliente(models.Model):
    PARTICULAR = 'P'
    EMPRESA = 'E'
    TIPO_CLIENTE = [
        (PARTICULAR, 'Particular'),
        (EMPRESA, 'Empresa'),
    ]
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=30)
    tipo = models.CharField(choices=TIPO_CLIENTE, default=PARTICULAR, max_length=1)
    edad = models.PositiveIntegerField(default=18)
    tarjeta_credito = models.CharField(max_length=16)
    carnet_de_conducir = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=300)

    def __str__(self):
        return str(self.nombre+"-"+str(self.id))

    def validate_tarjeta(self, value):
        #Validate using the Luhn algorithm
        #https://en.wikipedia.org/wiki/Luhn_algorithm        
        #Check if there are just only 16 chars
        if len(value) != 16:
            raise ValidationError(
            _('%(value)s has not 16 digits'),
            params={'value': value},
        )
        #Check if value is a number
        try:
            value = int(value)
        except ValueError:
            raise ValidationError(
            _('%(value)s is not a number'),
            params={'value': value},
        )
        
        checksum, factor = 0, 1
        for c in reversed(value):
            for c in str(factor * (int(c))):
                checksum += int(c)
            factor = 3-factor
        if checksum %10 != 0:
            raise ValidationError(_('%(value)s is not correct'), params={'value': value},)
'''
    def hash(password):
        return hashers.make_password(password=str(password))

    def save(self):
        self.contrasena = self.hash(self.contrasena)
        super(Cliente, self).save()'''


class Coche(models.Model):
    DISPONIBLE = 'D'
    REVISION_MANTENIMIENTO = 'M'
    REVISION_GOLPE = 'G'
    BAJA = 'B'
    RESERVADO = 'R'
    ESTADO_COCHE = [
        (DISPONIBLE, 'Disponible'),
        (REVISION_MANTENIMIENTO, 'Revision: Mantenimiento'),
        (REVISION_GOLPE, 'Revision: Golpe'),
        (BAJA, 'Baja'),
        (RESERVADO, 'Reservado'),
    ]
    CALENDARIO_DEFAULT = {datetime.date.today(), 'D'}
    modelo = models.ForeignKey(Modelo, on_delete=models.DO_NOTHING)
    categoria = models.CharField(choices=[('A', 'Alta'), ('M', 'Media'), ('B', 'Baja')], max_length=1)
    puertas = models.IntegerField(choices=[(3, 3), (5, 5)])
    techo = models.CharField(choices=[('N', 'Normal'), ('C', 'Cabrio-Descapotable'), ('S', 'Solar-Panoramico')], max_length=1)
    transmision = models.CharField(max_length=1, choices=[('M', 'Manual'), ('A', 'Automatico')])
    estado = models.CharField(max_length=1, choices=ESTADO_COCHE, default=DISPONIBLE)
    calendario = models.JSONField(default=str(CALENDARIO_DEFAULT))  # JSON que contendra los dias en los que el coche esta reservado o de baja

    def __str__(self):
        return str(Modelo.objects.get(id=self.modelo.id))+"-"+str(self.id)+"-"+str(self.estado)


class Reserva(models.Model):
    FRANQUICIAS = [('1', 'oficina 1'), ('2', 'oficina 2'), ('3', 'oficina 3'), ('4', 'oficina 4')]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    precio = models.FloatField(validators=[MinValueValidator(0.00)])
    fecha_reserva = models.DateField(default=datetime.date.today)
    fecha_objetivo = models.DateField()
    franquicia_recogida = models.CharField(max_length=30, choices=FRANQUICIAS, default='1')
    franquicia_entrega = models.CharField(max_length=30, choices=FRANQUICIAS, default='1')

    def get_precio(self):
        return self.precio

    def __str__(self):
        return str(Cliente.objects.get(id=self.cliente.id).nombre)+"-"+str(self.id)


class Factura(models.Model):
    EFECTIVO = 'E'
    VISA = 'V'
    MASTERCARD = 'MC'
    PAYPAL = 'PP'
    AMERICANEXPRESS = 'AE'
    TIPO_PAGO = [
        (EFECTIVO, 'Efectivo'),
        (VISA, 'Visa'),
        (MASTERCARD, 'Mastercard'),
        (PAYPAL, 'PayPal'),
        (AMERICANEXPRESS, 'American Express'),
    ]

    id_reserva = models.ForeignKey(Reserva, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(default=datetime.date.today, editable=False)
    importe = models.FloatField(default=None, editable=False)
    pago = models.CharField(choices=TIPO_PAGO, default=EFECTIVO, max_length=2)

    def save(self):
        if self.importe is None:
            self.importe = Reserva.objects.get(id=self.id_reserva.id).precio
        super(Factura, self).save()

    def __str__(self):
        return str(self.id)
