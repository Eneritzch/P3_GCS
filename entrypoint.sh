#!/bin/sh
# Punto de entrada del contenedor Django.
# 1) Espera a que PostgreSQL esté disponible.
# 2) Aplica migraciones y recolecta estáticos.
# 3) Ejecuta el comando recibido (CMD del Dockerfile / command de compose).
set -e

echo "==> Esperando a PostgreSQL en ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" > /dev/null 2>&1; do
  echo "    PostgreSQL no responde todavía, reintentando en 1s..."
  sleep 1
done
echo "==> PostgreSQL disponible."

echo "==> Aplicando migraciones..."
python manage.py migrate --noinput

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando aplicación: $@"
exec "$@"
