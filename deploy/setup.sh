#!/bin/bash
# =============================================================================
# Lightsail first-time setup for viktorija.vincegomez.com
# SSH into your Lightsail instance and run: bash deploy/setup.sh
# =============================================================================
set -e

APP_DIR="$HOME/viktorija-coaching"
DOMAIN="viktorija.vincegomez.com"
WEB_PORT=8010

echo "=== 1. Clone repo ==="
if [ ! -d "$APP_DIR" ]; then
    git clone https://github.com/VG2000/viktorija-coaching.git "$APP_DIR"
else
    echo "Repo already exists at $APP_DIR, pulling latest..."
    cd "$APP_DIR" && git pull origin main
fi

echo "=== 2. Create .env ==="
if [ ! -f "$APP_DIR/.env" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    cat > "$APP_DIR/.env" << ENVEOF
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_ALLOWED_HOSTS=$DOMAIN,localhost
CSRF_TRUSTED_ORIGINS=https://$DOMAIN
DJANGO_SETTINGS_MODULE=viktorijacoaching.settings.production
WAGTAILADMIN_BASE_URL=https://$DOMAIN
ENVEOF
    echo ".env created with auto-generated secret key"
else
    echo ".env already exists"
fi

echo "=== 3. Build and start containers ==="
cd "$APP_DIR"
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

echo "=== 4. Wait for containers to start ==="
sleep 5

echo "=== 5. Set up pages ==="
docker compose -f docker-compose.prod.yml exec web python setup_pages.py

echo "=== 6. Create superuser ==="
echo "Create your admin account:"
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

echo "=== 7. Configure nginx ==="
sudo cp "$APP_DIR/deploy/nginx.conf" "/etc/nginx/sites-available/$DOMAIN"
sudo ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
sudo nginx -t
sudo systemctl reload nginx

echo "=== 8. Get SSL certificate ==="
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email you@example.com || {
    echo "Certbot failed. Make sure DNS A record for $DOMAIN points to this server."
    echo "Run manually: sudo certbot --nginx -d $DOMAIN"
}

echo ""
echo "=== Done! ==="
echo "Site should be live at https://$DOMAIN"
echo "Admin: https://$DOMAIN/admin/"
echo ""
echo "Useful commands:"
echo "  cd $APP_DIR"
echo "  make prod-logs     # view logs"
echo "  make prod-deploy   # redeploy after changes"
