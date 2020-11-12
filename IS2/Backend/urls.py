from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('', views.home),
    path('register/', views.register, name="register"),
    # path('{user}/start/', views.start,)
]
