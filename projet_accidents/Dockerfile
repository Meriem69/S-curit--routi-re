# Image de base Python (version slim = légère)
FROM python:3.11-slim

# Labels (métadonnées)
LABEL maintainer="Leila, Caroline, Ina & Meriem"
LABEL version="1.0"
LABEL description="API de prédiction de gravité des accidents routiers"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail
WORKDIR /app

# Copier requirements en premier (optimisation cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]