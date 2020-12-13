import mimetypes
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from .models import *
from .forms import RegisterUserForm, LoginUserForm
from django.views.generic import ListView


def login(request):
    form = LoginUserForm
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        print('POST>', request.POST)
        try:
            if form.is_valid():
                uid = form.get_user_id()
                messages.success(request, 'User {} logged in'.format(uid))
                return redirect('user home', Cliente.objects.get(id=uid).id)
            else:
                context = {'form': LoginUserForm}
                # messages.error(request, 'Wrong Form data')
                return render(request, 'Backend/login.html', context)
        except Exception as e:
            print('Exception>> '+str(e))
            messages.error(request, 'Error on validating')
            context = {'form': LoginUserForm}
            return render(request, 'Backend/login.html', context)
    context = {'form': form}
    return render(request, 'Backend/login.html', context)


def home(request):
    context = {}
    return render(request, 'Backend/home.html')


def register(request):
    form = RegisterUserForm
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            uid = form.get_user_id()
            messages.success(request, 'User {} created'.format(uid))
            return redirect('user home', Cliente.objects.get(id=uid).id)
        else:
            messages.error(request, 'Wrong Form data')
            return render(request, 'Backend/register.html', context={'form': RegisterUserForm})

    context = {'form': form}
    return render(request, 'Backend/register.html', context)


def start(request, pk):
    if Cliente.objects.get(id=pk) is None:
        raise Http404('Usuario no registrado')
    context = {'pk': pk, 'cliente': Cliente.objects.get(id=pk), 'today': datetime.date.today(), 'marcas': Marca.objects.all(),
               'gamas': [('A', 'Alta'), ('M', 'Media'),
                         ('B', 'Baja')]}

    marca = request.GET.get('marcas', '')
    gama = request.GET.get('gamas', '')
    fecha_ini = request.GET.get('fecha_start', datetime.date.today())
    fecha_fin = request.GET.get('fecha_end', datetime.date.today())
    queryset = Coche.objects.all()
    if gama != '':
        context['current_gama'] = gama
        queryset = [i for i in queryset if i.categoria == gama[0]]
    if marca != '':
        context['current_marca'] = marca
        queryset = [i for i in queryset if i.modelo.marca_fk.marca == marca]
    context['object_list'] = queryset
    # TODO: Filtrar fechas de coches disponibles
    return render(request, 'Backend/startpage.html', context)


def create(request, pk):
    return render(request, 'Backend/createreserva.html')


def reservas(request, pk):
    if Cliente.objects.get(id=pk) is None:
        raise Http404('Usuario no registrado')
    context = {'pk': pk, 'cliente': Cliente.objects.get(id=pk)}
    queryset = [i for i in Reserva.objects.all() if i.cliente_id == pk]
    context['lista_reservas'] = queryset
    return render(request, 'Backend/consultarreserva.html', context)


def tarifas(request, pk):
    context = {}
    if Cliente.objects.get(id=pk) is None:
        raise Http404('Usuario no registrado')
    queryset = Tarifas.objects.all()
    context['tarifas'] = queryset
    context['pk'] = pk
    return render(request, 'Backend/tarifas.html', context)


def descargar_factura(request, pk, id_r):

    cliente = Cliente.objects.get(id=pk)
    reserva = Reserva.objects.get(id=id_r)
    factura = Factura.objects.get(id_reserva=id_r, id_reserva__cliente=pk)
    if cliente is None:
        raise Http404('Usuario no registrado')
    if reserva is None:
        raise Http404('Reserva no encontrada')
    if factura is None:
        raise Http404('Factura no generada, espere a administrador')

    path = os.getcwd()+'\\Backend\\migrations\\temp'
    filename = 'factura_web' + Cliente.objects.get(id=pk).nombre + '-' + str(id_r) + '.txt'

    with open(path+'\\'+filename, 'w') as fl:
        mensaje = 'Factura generada automaticamente por servicio web\n\nCliente: ' + cliente.nombre + ' ' + cliente.apellidos +\
                '\n\tImporte Factura: '+str(factura.importe)+'\n\tMetodo de pago: '+factura.pago + '\n\tFecha factura: ' + \
              str(factura.fecha) + '\n\tFecha reserva: ' + str(reserva.fecha_reserva) + '\n\tFecha inicio: ' + str(reserva.fecha_objetivo) \
              + '\n\tCoche Reservado: ' + str(reserva.coche) + '\n\tFranquicia entrega: ' + str(reserva.franquicia_entrega) + \
              '\n\tFranquicia recogida: ' + str(reserva.franquicia_recogida) + '\n\n\n\nGracias por usar nuestro servicio'
        fl.write(mensaje)

    fl = open(path+'\\'+filename, 'r')
    mime_type, _ = mimetypes.guess_type(path)
    response = HttpResponse(fl, content_type='text/plain')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    fl.close()
    os.remove(path+'\\'+filename)
    return response
