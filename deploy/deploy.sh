#!/bin/bash
# =============================================================================
# Redeploy viktorija.vincegomez.com after code changes
# Run as: bash deploy/deploy.sh
# =============================================================================
set -e

APP_DIR="$HOME/viktorija-coaching"
cd "$APP_DIR"

echo "=== Pulling latest code ==="
git pull origin main

echo "=== Building container ==="
docker compose -f docker-compose.prod.yml build web

echo "=== Starting services ==="
docker compose -f docker-compose.prod.yml up -d

echo "=== Collecting static files ==="
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo "=== Copying static files to host ==="
mkdir -p "$APP_DIR/staticfiles"
docker compose -f docker-compose.prod.yml cp web:/app/staticfiles/. "$APP_DIR/staticfiles/"

echo "=== Syncing media files to host ==="
mkdir -p "$APP_DIR/media"
docker compose -f docker-compose.prod.yml cp web:/app/media/. "$APP_DIR/media/" 2>/dev/null || true

echo ""
echo "=== Deploy complete ==="
docker compose -f docker-compose.prod.yml ps
