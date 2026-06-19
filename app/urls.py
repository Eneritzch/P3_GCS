"""URLs de la aplicación."""
from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.lista_tareas, name="lista_tareas"),
]
