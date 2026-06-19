"""Vistas de la aplicación."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TareaForm
from .models import Tarea


def lista_tareas(request):
    """Muestra la lista de tareas y el formulario para crear una nueva."""
    tareas = Tarea.objects.all()
    contexto = {
        "tareas": tareas,
        "form": TareaForm(),
        "total": tareas.count(),
        "completadas": tareas.filter(completada=True).count(),
        "pendientes": tareas.filter(completada=False).count(),
    }
    return render(request, "app/lista_tareas.html", contexto)


@require_POST
def crear_tarea(request):
    """Crea una nueva tarea a partir del formulario enviado."""
    form = TareaForm(request.POST)
    if form.is_valid():
        tarea = form.save()
        messages.success(request, f'Tarea "{tarea.titulo}" creada.')
    else:
        messages.error(request, "Revisa los datos: el título es obligatorio.")
    return redirect("app:lista_tareas")


@require_POST
def completar_tarea(request, pk):
    """Alterna el estado completada/pendiente de una tarea."""
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completada = not tarea.completada
    tarea.save()
    estado = "completada" if tarea.completada else "marcada como pendiente"
    messages.info(request, f'Tarea "{tarea.titulo}" {estado}.')
    return redirect("app:lista_tareas")


@require_POST
def eliminar_tarea(request, pk):
    """Elimina una tarea."""
    tarea = get_object_or_404(Tarea, pk=pk)
    titulo = tarea.titulo
    tarea.delete()
    messages.warning(request, f'Tarea "{titulo}" eliminada.')
    return redirect("app:lista_tareas")
