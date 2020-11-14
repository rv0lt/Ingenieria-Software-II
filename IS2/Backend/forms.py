from django.shortcuts import render
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'contrasena', 'tipo', 'edad', 'tarjeta_credito', 'carnet_de_conducir', 'direccion']


class RegisterUser(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellidos = forms.CharField(max_length=100)
    contrasena = forms.CharField(max_length=30, widget=forms.PasswordInput)
    contrasena2 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    edad = forms.IntegerField(min_value=16, max_value=99)
    tipo = forms.CharField(widget=forms.RadioSelect)
    tarjeta_credito = forms.CharField(max_length=16)
    carnet_de_conducir = forms.CharField(max_length=9)
    direccion = forms.CharField(max_length=300)

    def is_valid(self):
        return super().is_valid() and self.contrasena == self.contrasena2
