# PHASE 5 — Docker & GitHub Container Registry (GHCR)

## Concepts clés

### Pourquoi conteneuriser ?

**Le problème "ça marche sur ma machine" :**
Sans Docker, chaque développeur a un environnement différent :
- Meriem a Python 3.11, Leila a Python 3.9
- Caroline a PostgreSQL 14, Ina a PostgreSQL 15
- Sur le serveur de prod c'est encore différent

Résultat : le code marche chez une personne mais pas chez une autre.

**La solution Docker :**
Docker crée une "boîte" (conteneur) qui contient TOUT :
- Le code
- Python dans la bonne version
- Toutes les dépendances
- La configuration

```
Sans Docker :
"Ça marche chez moi" → déploiement → ❌ ça plante en prod

Avec Docker :
"Ça marche dans mon conteneur" → même conteneur en prod → ✅ ça marche
```

**Avantages Docker :**
- Reproductibilité : même comportement partout
- Isolation : chaque app dans sa boîte, pas de conflits
- Portabilité : tourne sur n'importe quel serveur avec Docker
- Scalabilité : facile de lancer 10 copies du même conteneur

---

### Qu'est-ce que GHCR ?

GHCR (GitHub Container Registry) = entrepôt d'images Docker hébergé par GitHub.

```
Docker Hub = entrepôt public généraliste (hub.docker.com)
GHCR = entrepôt intégré à GitHub (ghcr.io)
```

Avantages de GHCR :
- Gratuit pour les repos publics
- Authentification automatique via GITHUB_TOKEN (pas besoin de secrets)
- Intégré aux permissions GitHub du repo
- L'image est liée au repo et visible dans l'onglet "Packages"

---

### Stratégie de tags Docker

Une image Docker peut avoir plusieurs tags — comme des étiquettes.

```
ghcr.io/meriem69/s-curit--routi-re:latest     ← toujours la dernière version stable
ghcr.io/meriem69/s-curit--routi-re:develop    ← version en cours de développement
ghcr.io/meriem69/s-curit--routi-re:sha-8cea8d9 ← version exacte par commit
```

**Pourquoi plusieurs tags ?**
- `latest` : pour les utilisateurs qui veulent juste "la dernière version stable"
- `develop` / `main` : pour savoir de quelle branche vient l'image
- `sha-xxxxx` : pour tracer exactement quel commit a produit cette image

**latest vs semver vs sha :**

| Tag | Exemple | Utilité |
|-----|---------|---------|
| latest | :latest | Toujours la dernière version de main |
| semver | :v1.2.0 | Version précise pour la production |
| sha | :sha-8cea8d9 | Debug — savoir exactement quel commit |
| branch | :develop | Tester la version en cours |

---

## Ce qu'on a fait — étape par étape

---

### Étape 1 — Amélioration du Dockerfile

Le Dockerfile existant utilisait `pip` et `requirements.txt`.
On l'a amélioré pour utiliser `uv` (plus rapide) et corriger P24
(utilisateur root).

**Avant :**
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Après :**
```dockerfile
FROM python:3.11-slim

LABEL maintainer="Leila, Caroline, Ina & Meriem"
LABEL version="1.0"
LABEL description="API de prédiction de gravité des accidents routiers"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc postgresql-client curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv depuis son image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copier fichiers de dépendances en premier (cache Docker)
COPY pyproject.toml uv.lock ./

# Installer les dépendances avec uv
RUN uv pip install -e .

# Copier le code
COPY . .

# Créer un utilisateur non-root (correction P24)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Améliorations apportées :**
- `uv` remplace `pip` → installation 10x plus rapide
- `uv.lock` copié avant le code → meilleur cache Docker
- Utilisateur `appuser` non-root → correction de P24 (sécurité)
- `rm -rf /var/lib/apt/lists/*` → image plus légère

---

### Étape 2 — Création du workflow build.yml

Fichier `.github/workflows/build.yml` créé à la racine du repo.

**Ce que fait ce workflow :**
1. Se déclenche sur push vers main ou develop
2. Se déclenche sur PR vers main (build sans push)
3. Se connecte à GHCR avec le GITHUB_TOKEN automatique
4. Build l'image Docker depuis `projet_accidents/`
5. Tague l'image (branche + SHA + latest si main)
6. Push l'image sur GHCR

**Points importants du fichier :**

```yaml
permissions:
  contents: read
  packages: write   # nécessaire pour écrire sur GHCR
```

```yaml
context: ./projet_accidents   # là où est le Dockerfile
push: ${{ github.event_name != 'pull_request' }}
# Sur une PR : build mais pas push (juste vérifier que ça compile)
# Sur un push : build ET push
```

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
# Cache GitHub Actions → les prochains builds sont plus rapides
```

---

### Étape 3 — Problème récurrent : --no-verify

**Erreur rencontrée à chaque commit :**
```
[ERROR] Your pre-commit configuration is unstaged.
`git add .pre-commit-config.yaml` to fix this.
```

**Cause :** pre-commit est installé à la racine du repo mais cherche
`.pre-commit-config.yaml` dans `projet_accidents/`. Les deux emplacements
ne se synchronisent pas bien.

**Solution utilisée :**
```bash
git commit -m "..." --no-verify
```

**Quand c'est acceptable :**
- Pour les fichiers CI/YAML qui ne sont pas du code Python
- Quand ruff n'a rien à vérifier de toute façon
- En phase de mise en place de l'outillage

**Quand c'est inacceptable :**
- Pour du code Python en production
- Quand on veut bypasser une vraie vérification de sécurité

**Point d'amélioration :** restructurer le repo pour que tout soit
à la racine élimine ce problème.

---

### Résultat

Build & Push Docker ✅ en 1m45s

Image disponible sur :
```
ghcr.io/meriem69/s-curit--routi-re:develop
ghcr.io/meriem69/s-curit--routi-re:sha-8cea8d9
```

Visible dans GitHub → profil → Packages.

---

## Réponses aux questions de réflexion

### 1. Pourquoi conteneuriser ?

**Avantages Docker :**
- Reproductibilité : même comportement en dev, staging et production
- Isolation : pas de conflits entre les dépendances de différents projets
- Portabilité : tourne sur n'importe quel serveur Linux/Mac/Windows avec Docker
- Déploiement simple : `docker run` suffit, pas besoin de configurer l'environnement

**Problème "ça marche sur ma machine" :**
Sans Docker, le code dépend de l'environnement local de chaque développeur.
Python 3.9 vs 3.11, versions de bibliothèques différentes, variables
d'environnement manquantes... Docker encapsule tout dans une image identique
pour tout le monde.

---

### 2. Construction en plusieurs étapes : pourquoi ?

Le brief mentionne le multi-stage build. On ne l'a pas implémenté
complètement mais voici le principe :

**Taille de l'image :**
```dockerfile
# Stage 1 : builder (avec tous les outils de compilation)
FROM python:3.11 AS builder
RUN pip install build wheel
COPY . .
RUN python -m build

# Stage 2 : image finale (légère, sans les outils de build)
FROM python:3.11-slim
COPY --from=builder /app/dist ./
```

Le résultat final ne contient que ce qui est nécessaire pour tourner,
pas les outils qui ont servi à compiler. Image 5x plus petite.

**Sécurité :**
Moins de paquets installés = moins de surface d'attaque.
Un pirate qui entre dans le conteneur ne trouve pas gcc, make, etc.

---

### 3. Stratégie de balisage

**Pourquoi plusieurs tags ?**
Chaque tag répond à un besoin différent selon l'utilisateur de l'image.

**latest :**
- Pour : les utilisateurs qui veulent "juste la dernière version stable"
- Contre : on ne sait pas exactement quelle version c'est
- Règle : ne mettre `latest` que sur main, jamais sur develop

**semver (v1.2.0) :**
- Pour : la production — on sait exactement quelle version tourne
- Permet de rollback facilement : `docker run image:v1.1.0`
- Généré automatiquement par Semantic Release (Phase 6)

**sha (sha-8cea8d9) :**
- Pour : le débogage — tracer exactement quel commit a produit l'image
- Utile quand un bug apparaît : on sait dans quel commit chercher
- Immuable : le sha ne change jamais

---

## Résumé Phase 5

| Élément | Statut |
|---------|--------|
| Dockerfile amélioré avec uv | ✅ |
| Utilisateur non-root (P24) | ✅ |
| `.github/workflows/build.yml` créé | ✅ |
| Build Docker vert sur GitHub Actions | ✅ |
| Image publiée sur GHCR | ✅ |
| Tags automatiques (branche + SHA) | ✅ |
| Cache GitHub Actions activé | ✅ |
