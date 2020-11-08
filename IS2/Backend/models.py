from django.db import models
from django import forms


class Cliente(models.Model):
    PARTICULAR = 'P'
    EMPRESA = 'E'
    TIPO_CLIENTE = [
        (PARTICULAR, 'Particular'),
        (EMPRESA, 'Empresa'),
    ]
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    tipo = models.TextField(choices=TIPO_CLIENTE, default=PARTICULAR, max_length=10)
    edad = models.IntegerField(default=18)
    tarjeta_credito = models.CharField(max_length=16)
    carnet_de_conducir = models.CharField(max_length=9)  # dni?
    direccion = models.CharField(max_length=300)

    # tipo = forms.ChoiceField(choices=TIPO_CLIENTE, widget=forms.RadioSelect())

    def __str__(self):
        return str(id(self))