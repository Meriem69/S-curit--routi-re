# Image de base Python
FROM python:3.11-slim

# Labels
LABEL maintainer="Leila, Caroline, Ina & Meriem"
LABEL version="1.0"
LABEL description="API de prédiction de gravité des accidents routiers"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copier les fichiers de dépendances en premier (optimisation cache)
COPY pyproject.toml uv.lock ./

# Installer les dépendances
RUN uv pip install -e .

# Copier le reste de l'application
COPY . .

# Créer un utilisateur non-root (sécurité P24)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]