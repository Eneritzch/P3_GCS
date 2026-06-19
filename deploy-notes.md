# 📦 Notas de Despliegue Simulado — Flujo CI/CD para Django

Este documento describe cómo se **despliega** el proyecto a partir del flujo
automatizado de CI/CD. La idea es simular lo que haría un servidor de producción:
obtener el proyecto/imagen, levantarlo con Docker Compose y validarlo en el
navegador.

---

## 1. ¿Qué produce el flujo automatizado?

El workflow `.github/workflows/ci.yml` tiene dos etapas:

1. **`test`** → instala dependencias y ejecuta `python manage.py test` contra
   un PostgreSQL real. Si fallan los tests, el pipeline se detiene.
2. **`build`** → (solo si `test` pasa) construye la imagen Docker y la guarda
   como **artefacto** llamado `imagen-docker-django` (`gcs-web-image.tar`).
   Además imprime los pasos *simulados* de publicación en DockerHub.

> El artefacto queda disponible para descarga en:
> **GitHub → pestaña Actions → (run) → sección Artifacts**

---

## 2. Despliegue simulado — Opción A: desde el código (git clone)

Simula un servidor que clona el repositorio y lo levanta con Docker Compose.

```bash
# 1) Crear una carpeta EXTERNA al proyecto (simula el servidor de despliegue)
mkdir C:\despliegue_gcs
cd C:\despliegue_gcs

# 2) Descargar el proyecto desde GitHub
git clone https://github.com/Eneritzch/P3_GCS.git
cd P3_GCS

# 3) Levantar la aplicación con Docker Compose (construye y arranca)
docker compose up -d --build

# 4) Verificar que los contenedores están corriendo
docker compose ps

# 5) Validar desde el navegador
#    Abrir: http://localhost:8000
```

Para detener el despliegue:

```bash
docker compose down        # detiene y elimina contenedores (conserva datos)
docker compose down -v     # además borra el volumen de la base de datos
```

---

## 3. Despliegue simulado — Opción B: desde el artefacto (imagen .tar)

Simula un servidor que **no compila**, sino que recibe la imagen ya construida
por el pipeline (como llegaría desde DockerHub o el artefacto de GitHub).

```bash
# 1) Descargar el artefacto 'imagen-docker-django' desde la pestaña Actions
#    y descomprimirlo para obtener gcs-web-image.tar

# 2) Cargar la imagen en Docker local
docker load -i gcs-web-image.tar

# 3) Confirmar que la imagen está disponible
docker images gcs-web

# 4) Levantar con Docker Compose (usa la imagen ya cargada)
docker compose up -d

# 5) Validar en el navegador: http://localhost:8000
```

---

## 4. Validación del despliegue

Una vez levantado, se valida que la aplicación responde correctamente:

| Verificación              | Comando / Acción                          | Resultado esperado            |
| ------------------------- | ----------------------------------------- | ----------------------------- |
| Contenedores arriba       | `docker compose ps`                       | `gcs_web` y `gcs_db` = Up     |
| Servidor escuchando       | `docker compose logs web`                 | "Listening at: 0.0.0.0:8000"  |
| Respuesta HTTP            | Navegador en `http://localhost:8000`      | Página "Gestión de Tareas"    |
| Funcionalidad (CRUD)      | Crear / completar / eliminar una tarea    | La lista se actualiza         |
| Persistencia              | `docker compose down` y `up` de nuevo     | Las tareas se conservan       |

---

## 5. Mapeo de puertos (por qué el navegador ve el contenedor)

En `docker-compose.yml`:

```yaml
ports:
  - "8000:8000"   # PUERTO_HOST : PUERTO_CONTENEDOR
```

El puerto **8000 de tu máquina** se redirige al **8000 del contenedor `gcs_web`**,
donde Gunicorn sirve la aplicación Django. Por eso `http://localhost:8000`
muestra lo que corre dentro del contenedor.

---

## 6. Variables de entorno usadas en el despliegue

| Variable             | Descripción                          | Valor en compose |
| -------------------- | ------------------------------------ | ---------------- |
| `DJANGO_SECRET_KEY`  | Clave secreta de Django              | (definida)       |
| `DJANGO_DEBUG`       | Modo depuración                      | `True` (demo)    |
| `POSTGRES_HOST`      | Host de la base de datos             | `db`             |
| `POSTGRES_DB`        | Nombre de la base de datos           | `gcs_db`         |
| `POSTGRES_USER`      | Usuario de la base de datos          | `gcs_user`       |
| `POSTGRES_PASSWORD`  | Contraseña de la base de datos       | `gcs_pass`       |

> En producción, `DJANGO_DEBUG` debe ser `False` y los secretos deben venir de
> un gestor de secretos, no del archivo compose.
