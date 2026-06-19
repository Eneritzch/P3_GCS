"""URLs de la aplicación."""
from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.lista_tareas, name="lista_tareas"),
    path("crear/", views.crear_tarea, name="crear_tarea"),
    path("completar/<int:pk>/", views.completar_tarea, name="completar_tarea"),
    path("eliminar/<int:pk>/", views.eliminar_tarea, name="eliminar_tarea"),
]
