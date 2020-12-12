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
    context = {'cliente': Cliente.objects.get(id=pk), 'today': datetime.date.today(), 'marcas': Marca.objects.all(),
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
