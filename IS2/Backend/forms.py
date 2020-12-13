from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Coche, Reserva
from django import forms
from django.forms import ModelForm, CharField, IntegerField, PasswordInput, NumberInput


class RegisterUserForm(forms.ModelForm):
    contrasena2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'})
                                  , label='')
    edad = forms.IntegerField(label='', min_value=16, max_value=99,
                              widget=forms.NumberInput(attrs={'placeholder': 'Edad'}))

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'contrasena', 'contrasena2', 'edad', 'tarjeta_credito', 'carnet_de_conducir',
                  'direccion', 'tipo')
        labels = {
            'nombre': '',
            'apellidos': '',
            'contrasena': '',
            'contrasena2': '',
            'edad': '',
            'tarjeta_credito': '',
            'carnet_de_conducir': '',
            'tipo': '',
            'direccion': '',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'contrasena': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'edad': forms.NumberInput(attrs={'placeholder': 'Edad', 'min': '16', 'max': '100'}),
            'tarjeta_credito': forms.TextInput(attrs={'placeholder': 'Tarjeta de Credito'}),
            'carnet_de_conducir': forms.TextInput(attrs={'placeholder': 'Carnet de conducir (DNI)', 'pattern':
                '(([x-z]|[X-Z]{1})([-]?)(\d{7})([-]?)([a-z]|[A-Z]{1}))|((\d{8})([-]?)([a-z]|[A-Z]{1}))'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Direccion'}),
            'tipo': forms.Select(choices=[('P', 'Particular'), ('E', 'Empresa')], attrs={'class': 'select'}),
        }

    def is_valid(self):
        return super().is_valid() and self.cleaned_data.get('contrasena') == self.cleaned_data.get('contrasena2')

    def get_user_id(self):
        return Cliente.objects.get(carnet_de_conducir=self.cleaned_data['carnet_de_conducir']).id


class LoginUserForm(forms.Form):
    user_id = forms.CharField(label='', max_length=9, widget=forms.TextInput({'placeholder': 'Id Usuario (DNI/NIE)'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def get_user_id(self):
        return Cliente.objects.get(carnet_de_conducir=self.cleaned_data['user_id']).id

    def clean(self):
        cd = self.cleaned_data
        uid = cd.get('user_id')
        p1 = cd.get('password')
        if Cliente.objects.get(carnet_de_conducir=uid).contrasena != p1:
            raise ValidationError("Contraseña no coincidente")
        return cd


'''
    def is_valid(self):
        # return Cliente.objects.get(carnet_de_conducir=self.user_id).contrasena == Cliente.hash(self.password)
        return Cliente.objects.get(carnet_de_conducir=self.cleaned_data['user_id']).contrasena == self.cleaned_data['password']
'''


class DateInput(forms.DateInput):
    input_type = 'date'


class ReservaForm(forms.Form):
    # FRANQUICIAS = [('1', 'oficina 1'), ('2', 'oficina 2'), ('3', 'oficina 3'), ('4', 'oficina 4')]
    EXTRAS = [('NAV', 'Navegador'), ('CAD', 'Cadenas de nieve'), ('NIN', 'Asiento de niño'), ('SEG', 'Seguro adicional')]

    car = forms.ModelChoiceField(queryset=Coche.objects.all().order_by('modelo'))
    date_recogida = forms.DateField(widget=DateInput)
    date_deposicion = forms.DateField(widget=DateInput)
    franquicia_recogida = forms.ChoiceField(choices=Reserva.FRANQUICIAS)
    franquicia_desposicion = forms.ChoiceField(choices=Reserva.FRANQUICIAS)
    extras = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=EXTRAS)

     
