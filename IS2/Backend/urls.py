from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('', views.home),
    path('register/', views.register, name="register"),
    path('<int:pk>/start/', views.start, name="user home"),
    path('<int:pk>/createreserva/', views.create, name="create reserva"),
    path('<int:pk>/misreservas/', views.reservas, name="reservas"),
    path('<int:pk>/tarifas/', views.tarifas, name="tarifas"),
    path('<int:pk>/misreservas/<int:id_r>/generar', views.descargar_factura, name="factura generador")
]
