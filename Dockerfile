# Stage 1: Build TailwindCSS
FROM node:22-alpine AS tailwind
WORKDIR /build
COPY tailwind.config.js .
COPY viktorijacoaching/static/css/input.css viktorijacoaching/static/css/
COPY viktorijacoaching/templates/ viktorijacoaching/templates/
COPY home/templates/ home/templates/
COPY pages/templates/ pages/templates/
RUN npx tailwindcss@3 -i viktorijacoaching/static/css/input.css -o viktorijacoaching/static/css/output.css --minify

# Stage 2: Python application
FROM python:3.14-slim-bookworm AS production

RUN useradd --create-home appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=viktorijacoaching.settings.production

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .
COPY --from=tailwind /build/viktorijacoaching/static/css/output.css viktorijacoaching/static/css/output.css

RUN mkdir -p /app/data /app/media && chown -R appuser:appuser /app/data /app/media

RUN DJANGO_SECRET_KEY=build-only-not-real \
    DJANGO_ALLOWED_HOSTS=localhost \
    DATABASE_URL=sqlite:///tmp/db.sqlite3 \
    python manage.py collectstatic --noinput \
    && chown -R appuser:appuser /app/static

COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
