"""Vistas de la aplicación."""
from django.shortcuts import render

from .models import Tarea


def lista_tareas(request):
    """Muestra la lista de tareas registradas."""
    tareas = Tarea.objects.all()
    contexto = {
        "tareas": tareas,
        "total": tareas.count(),
        "completadas": tareas.filter(completada=True).count(),
    }
    return render(request, "app/lista_tareas.html", contexto)
