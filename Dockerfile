# Imagen base con Python 3.10 (requisito del proyecto)
FROM python:3.10-slim

# Evita archivos .pyc y fuerza salida sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Dependencias del sistema:
#   - postgresql-client: provee 'pg_isready' usado por el entrypoint
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python primero (mejor cacheo de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Normaliza el script a saltos de línea Unix y lo hace ejecutable
RUN sed -i 's/\r$//' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Puerto donde escucha la aplicación
EXPOSE 8000

# El entrypoint espera a la BD, migra y luego ejecuta el CMD
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto: servidor de producción Gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
