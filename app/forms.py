"""Formularios de la aplicación."""
from django import forms

from .models import Tarea


class TareaForm(forms.ModelForm):
    """Formulario para crear/editar una tarea."""

    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "placeholder": "¿Qué hay que hacer?",
                    "autofocus": True,
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Detalle (opcional)",
                    "rows": 2,
                }
            ),
        }
