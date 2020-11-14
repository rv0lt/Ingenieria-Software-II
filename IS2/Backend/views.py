from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .models import *


def login(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'Backend/login.html', context)


def home(request):
    context = {}
    return render(request, 'Backend/home.html')


def register(request):
    context = {}
    return render(request, 'Backend/register.html')


def start(request, user_id):
    context = {}
    return render(request, 'Backend/startpage.html')