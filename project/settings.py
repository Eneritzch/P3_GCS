"""
Configuración de Django para el proyecto.

Las variables sensibles y de entorno se leen desde variables de entorno,
de modo que el mismo código funcione en local, en Docker y en GitHub Actions.
"""
import os
from pathlib import Path

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: en producción la clave debe venir de una variable de entorno
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-clave-solo-para-desarrollo"
)

# DEBUG se desactiva poniendo DJANGO_DEBUG=False en el entorno
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0"
).split(",")


# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps propias
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Base de datos
# Por defecto usa PostgreSQL (requisito del proyecto). Para correr los tests
# en local sin levantar Postgres se puede poner USE_SQLITE=True.
if os.environ.get("USE_SQLITE", "False") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "gcs_db"),
            "USER": os.environ.get("POSTGRES_USER", "gcs_user"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "gcs_pass"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }


# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]


# Internacionalización
LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True


# Archivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
