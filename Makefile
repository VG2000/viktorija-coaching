COMPOSE_DEV = docker compose
COMPOSE_PROD = docker compose -f docker-compose.prod.yml

# ===========================================================================
# Local Development
# ===========================================================================
dev:
	.venv/bin/python manage.py runserver

tailwind:
	npx tailwindcss@3 -i viktorijacoaching/static/css/input.css -o viktorijacoaching/static/css/output.css --watch

tailwind-build:
	npx tailwindcss@3 -i viktorijacoaching/static/css/input.css -o viktorijacoaching/static/css/output.css --minify

migrate:
	.venv/bin/python manage.py migrate

superuser:
	.venv/bin/python manage.py createsuperuser

setup-pages:
	.venv/bin/python setup_pages.py

lint:
	ruff check --fix .
	ruff format .

# ===========================================================================
# Docker Local (dev with postgres + nginx)
# ===========================================================================
up:
	$(COMPOSE_DEV) up -d

down:
	$(COMPOSE_DEV) down

build:
	$(COMPOSE_DEV) build

logs:
	$(COMPOSE_DEV) logs -f web

docker-setup:
	$(COMPOSE_DEV) exec web python manage.py migrate
	$(COMPOSE_DEV) exec web python setup_pages.py

docker-superuser:
	$(COMPOSE_DEV) exec web python manage.py createsuperuser

# ===========================================================================
# Production (Lightsail Instance via SSH)
# ===========================================================================
prod-deploy: prod-pull prod-build prod-up prod-static prod-cleanup
	@echo "Deploy complete"

prod-pull:
	git pull origin main

prod-build:
	$(COMPOSE_PROD) build web

prod-up:
	$(COMPOSE_PROD) up -d

prod-down:
	$(COMPOSE_PROD) down

prod-restart:
	$(COMPOSE_PROD) restart web

prod-logs:
	$(COMPOSE_PROD) logs -f web

prod-shell:
	$(COMPOSE_PROD) exec web python manage.py shell

prod-migrate:
	$(COMPOSE_PROD) exec web python manage.py migrate

prod-static:
	mkdir -p staticfiles
	$(COMPOSE_PROD) cp web:/app/static/. ./staticfiles/

prod-nginx:
	sudo cp deploy/nginx.conf /etc/nginx/sites-available/viktorija.vincegomez.com
	sudo ln -sf /etc/nginx/sites-available/viktorija.vincegomez.com /etc/nginx/sites-enabled/
	sudo nginx -t
	sudo systemctl reload nginx

prod-createsuperuser:
	$(COMPOSE_PROD) exec web python manage.py createsuperuser

prod-setup-pages:
	$(COMPOSE_PROD) exec web python setup_pages.py

prod-status:
	$(COMPOSE_PROD) ps
	@echo ""
	@echo "Disk:"
	@df -h / | tail -1
	@echo ""
	@echo "Memory:"
	@free -h | head -2

prod-cleanup:
	docker system prune -f

prod-setup: prod-build prod-up prod-setup-pages prod-static prod-nginx prod-createsuperuser
	@echo "First-time setup complete"

# ===========================================================================
# Help
# ===========================================================================
help:
	@echo "Viktorija Coaching - Available Commands"
	@echo ""
	@echo "Local Development:"
	@echo "  make dev              Start Django dev server"
	@echo "  make tailwind         Watch & compile TailwindCSS"
	@echo "  make migrate          Run database migrations"
	@echo "  make superuser        Create admin superuser"
	@echo ""
	@echo "Docker Local:"
	@echo "  make up / down        Start/stop containers"
	@echo "  make build            Build Docker image"
	@echo "  make docker-setup     Migrate + create pages"
	@echo "  make docker-superuser Create superuser in Docker"
	@echo "  make logs             Tail web container logs"
	@echo ""
	@echo "Production (on Lightsail instance):"
	@echo "  make prod-deploy      Pull, build, restart, collect static"
	@echo "  make prod-setup       First-time full setup"
	@echo "  make prod-logs        View production logs"
	@echo "  make prod-status      Check containers + disk + memory"
	@echo "  make prod-nginx       Update nginx config"
