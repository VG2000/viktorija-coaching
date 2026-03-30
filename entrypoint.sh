#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Setting up initial pages..."
python setup_pages.py

echo "Starting gunicorn..."
exec gunicorn viktorijacoaching.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120
