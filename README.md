# P3_GCS — Sistema de Gestión de Tareas (Django) con CI/CD

Aplicación web **Django + PostgreSQL** (CRUD de tareas) con un pipeline completo de
**CI/CD** usando **GitHub Actions** y **Docker**.

![CI/CD](https://github.com/Eneritzch/P3_GCS/actions/workflows/ci.yml/badge.svg)

## ✨ Funcionalidad

- Crear, completar/reabrir y eliminar tareas.
- Contadores de tareas totales / completadas / pendientes.
- Panel de administración de Django (`/admin`).

## 🧱 Tecnologías

| Capa | Herramienta |
|------|-------------|
| Backend | Django 5.1 (Python 3.10) |
| Base de datos | PostgreSQL 15 |
| Servidor app | Gunicorn |
| Contenedores | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## 🚀 Cómo ejecutarlo

### Opción A — Docker (recomendada)

```bash
docker compose up -d --build
# Navegador → http://localhost:8000
```

### Opción B — Local con entorno virtual

```bash
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
set USE_SQLITE=True              # usa SQLite para probar sin Postgres
python manage.py migrate
python manage.py runserver
```

## ✅ Pruebas

```bash
set USE_SQLITE=True
python manage.py test
```

## 🔁 Pipeline CI/CD

Definido en [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

1. **`test`** — instala dependencias y corre las pruebas contra PostgreSQL.
2. **`build`** — (si los tests pasan) construye la imagen Docker, la guarda como
   artefacto y simula la publicación en DockerHub.

## 📚 Documentación

- [DOCUMENTACION_CICD.md](DOCUMENTACION_CICD.md) — documento técnico del pipeline.
- [Flujo_CICD_Django.pdf](Flujo_CICD_Django.pdf) — versión PDF.
- [deploy-notes.md](deploy-notes.md) — pasos del despliegue simulado.

## 📂 Estructura

```
P3_GCS/
├── manage.py · requirements.txt
├── project/        # settings, urls, wsgi/asgi
├── app/            # models, views, forms, urls, tests, templates
├── Dockerfile · docker-compose.yml · entrypoint.sh
└── .github/workflows/ci.yml
```
