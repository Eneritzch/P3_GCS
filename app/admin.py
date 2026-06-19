"""Registro de modelos en el panel de administración."""
from django.contrib import admin

from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "completada", "creada_en")
    list_filter = ("completada",)
    search_fields = ("titulo", "descripcion")
