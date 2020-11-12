from django.shortcuts import render
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'contrasena', 'tipo', 'edad', 'tarjeta_credito', 'carnet_de_conducir', 'direccion']
