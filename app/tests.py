"""Pruebas automatizadas de la aplicación."""
from django.test import TestCase
from django.urls import reverse

from .models import Tarea


class TareaModelTest(TestCase):
    """Pruebas sobre el modelo Tarea."""

    def setUp(self):
        self.tarea = Tarea.objects.create(
            titulo="Configurar CI/CD",
            descripcion="Crear el pipeline con GitHub Actions y Docker",
        )

    def test_creacion_tarea(self):
        """La tarea se crea con los valores esperados."""
        self.assertEqual(self.tarea.titulo, "Configurar CI/CD")
        self.assertFalse(self.tarea.completada)
        self.assertIsNotNone(self.tarea.creada_en)

    def test_str_devuelve_titulo(self):
        """El método __str__ devuelve el título de la tarea."""
        self.assertEqual(str(self.tarea), "Configurar CI/CD")

    def test_marcar_completada(self):
        """Una tarea puede marcarse como completada."""
        self.tarea.completada = True
        self.tarea.save()
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)


class ListaTareasViewTest(TestCase):
    """Pruebas sobre la vista de lista de tareas."""

    def setUp(self):
        Tarea.objects.create(titulo="Tarea A")
        Tarea.objects.create(titulo="Tarea B", completada=True)

    def test_vista_responde_200(self):
        """La vista de lista responde con código 200."""
        respuesta = self.client.get(reverse("app:lista_tareas"))
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_usa_template_correcta(self):
        """La vista usa la plantilla esperada."""
        respuesta = self.client.get(reverse("app:lista_tareas"))
        self.assertTemplateUsed(respuesta, "app/lista_tareas.html")

    def test_contexto_cuenta_tareas(self):
        """El contexto refleja el número correcto de tareas."""
        respuesta = self.client.get(reverse("app:lista_tareas"))
        self.assertEqual(respuesta.context["total"], 2)
        self.assertEqual(respuesta.context["completadas"], 1)
        self.assertEqual(respuesta.context["pendientes"], 1)


class CrearTareaViewTest(TestCase):
    """Pruebas sobre la creación de tareas."""

    def test_crear_tarea_valida(self):
        """Un POST válido crea la tarea y redirige."""
        respuesta = self.client.post(
            reverse("app:crear_tarea"),
            {"titulo": "Nueva tarea", "descripcion": "Detalle"},
        )
        self.assertRedirects(respuesta, reverse("app:lista_tareas"))
        self.assertEqual(Tarea.objects.count(), 1)
        self.assertEqual(Tarea.objects.first().titulo, "Nueva tarea")

    def test_crear_tarea_sin_titulo_no_crea(self):
        """Un POST sin título no crea ninguna tarea."""
        self.client.post(reverse("app:crear_tarea"), {"titulo": ""})
        self.assertEqual(Tarea.objects.count(), 0)


class CompletarTareaViewTest(TestCase):
    """Pruebas sobre el cambio de estado de una tarea."""

    def setUp(self):
        self.tarea = Tarea.objects.create(titulo="Pendiente")

    def test_completar_alterna_estado(self):
        """El POST alterna el estado completada de la tarea."""
        url = reverse("app:completar_tarea", args=[self.tarea.pk])
        self.client.post(url)
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)
        self.client.post(url)
        self.tarea.refresh_from_db()
        self.assertFalse(self.tarea.completada)


class EliminarTareaViewTest(TestCase):
    """Pruebas sobre la eliminación de tareas."""

    def setUp(self):
        self.tarea = Tarea.objects.create(titulo="A eliminar")

    def test_eliminar_tarea(self):
        """El POST elimina la tarea y redirige."""
        url = reverse("app:eliminar_tarea", args=[self.tarea.pk])
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse("app:lista_tareas"))
        self.assertEqual(Tarea.objects.count(), 0)

    def test_get_no_elimina(self):
        """Un GET no debe eliminar (solo se permite POST)."""
        url = reverse("app:eliminar_tarea", args=[self.tarea.pk])
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 405)
        self.assertEqual(Tarea.objects.count(), 1)
