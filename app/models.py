"""Modelos de la aplicación."""
from django.db import models


class Tarea(models.Model):
    """Una tarea simple dentro del sistema de gestión."""

    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField("Descripción", blank=True)
    completada = models.BooleanField("Completada", default=False)
    creada_en = models.DateTimeField("Creada en", auto_now_add=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["-creada_en"]

    def __str__(self):
        return self.titulo
