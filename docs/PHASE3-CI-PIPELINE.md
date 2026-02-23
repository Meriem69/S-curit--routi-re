# PHASE 3 — Pipeline CI : Tests, Qualité et Sécurité

## Concepts clés

### Qu'est-ce que GitHub Actions ?

GitHub Actions c'est un système d'automatisation intégré à GitHub.
Tu crées un fichier `.github/workflows/ci.yml` et GitHub le lit automatiquement
à chaque push ou Pull Request pour exécuter des vérifications sur ses propres serveurs.

```
Tu fais git push
      ↓
GitHub détecte le push
      ↓
GitHub lit .github/workflows/ci.yml
      ↓
GitHub lance 4 jobs en parallèle sur ses serveurs :
  ├── lint (ruff)
  ├── typecheck (mypy)
  ├── security (bandit)
  └── tests (pytest)
      ↓
Résultat : ✅ vert ou ❌ rouge sur ta PR
```

### Pourquoi plusieurs jobs séparés ?

**Avantages du parallélisme :** les 4 jobs tournent EN MÊME TEMPS.
Si tu mettais tout en un seul job, il faudrait attendre que lint finisse
avant de lancer les tests. Avec 4 jobs parallèles, tout tourne en 15-20 secondes
au lieu de 1 minute.

**Facilité de débogage :** si la CI échoue, tu vois immédiatement QUEL job
a échoué. "lint échoue" → problème de formatage. "tests échoue" → problème
dans le code. Pas besoin de lire 200 lignes de logs pour trouver.

### Qu'est-ce que le mock dans les tests ?

Mocker = simuler une dépendance externe sans vraiment l'utiliser.

```python
# Sans mock : le test dépend de PostgreSQL
# Si PostgreSQL ne tourne pas → test échoue
# Mais est-ce le code ou la BDD qui a un problème ? On ne sait pas.

# Avec mock : on simule que la BDD répond toujours correctement
# Si le test échoue → forcément le code qui est cassé
with patch("app_fastapi.save_prediction"):
    response = client.post("/predict", json={...})
```

C'est la bonne pratique pour les tests unitaires. Les tests qui utilisent
une vraie BDD s'appellent des tests d'intégration — c'est une autre catégorie.

---

## Ce qu'on a fait — étape par étape

---

### Étape 1 — Écriture des tests

On a découvert que le projet n'avait aucun test. On a créé les tests
en même temps que la CI — c'est une bonne pratique d'apprendre à écrire
des tests au moment où on configure la CI.

**Problème rencontré :** numpy et les autres dépendances n'étaient pas
installées dans l'environnement uv. On a dû les ajouter :

```bash
uv add numpy joblib scikit-learn fastapi uvicorn psycopg2-binary jinja2 python-multipart
```

**Pourquoi ce problème ?** Le projet utilisait `requirements.txt` avant.
Quand on a initialisé uv en Phase 1, l'environnement uv était vide —
il ne connaissait pas encore les dépendances du projet.

---

### Étape 2 — Création de la structure des tests

```bash
git checkout develop
git checkout -b feature/add-tests
mkdir tests
type nul > tests\__init__.py
type nul > tests\test_api.py
uv add --dev pytest pytest-cov httpx
```

**Pourquoi httpx ?** FastAPI utilise httpx pour son client de test.
Sans httpx, impossible d'utiliser `TestClient` de FastAPI.

---

### Étape 3 — Contenu des tests

4 tests écrits dans `tests/test_api.py` :

```python
# TEST 1 : /health retourne status ok
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# TEST 2 : /predict retourne une prédiction valide
def test_predict_json(client):
    with patch("app_fastapi.save_prediction"):
        response = client.post("/predict", json={...})
    assert response.status_code == 200
    assert "prediction" in response.json()

# TEST 3 : quand le modèle prédit 1, le label est GRAVE
def test_predict_returns_grave(client):
    ...
    assert response.json()["label"] == "GRAVE"

# TEST 4 : la page d'accueil retourne du HTML
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

Résultat en local :
```
4 passed in 2.19s
```

---

### Étape 4 — Création du fichier CI

```bash
git checkout develop
git checkout -b feature/add-ci-pipeline
mkdir .github
mkdir .github\workflows
```

Fichier `.github/workflows/ci.yml` créé avec 4 jobs :

**Structure du fichier :**
```yaml
name: CI

on:
  push:
    branches: [main, develop]    # se déclenche sur chaque push
  pull_request:
    branches: [main, develop]    # se déclenche sur chaque PR

defaults:
  run:
    working-directory: projet_accidents  # tous les jobs s'exécutent ici

jobs:
  lint:       # ruff check + ruff format
  typecheck:  # mypy (continue-on-error)
  security:   # bandit (continue-on-error)
  tests:      # pytest avec coverage
```

**Pourquoi `continue-on-error` sur mypy et bandit ?**
Le code a peu d'annotations de types et des problèmes de sécurité connus
(debug=True, 0.0.0.0...). On ne veut pas que ces jobs bloquent la CI
pour l'instant — on les corrigera progressivement.

---

### Étape 5 — Problème : fichier CI au mauvais endroit

**Problème découvert :** le fichier `ci.yml` avait été commité dans
`projet_accidents/.github/workflows/` au lieu de `.github/workflows/`
à la racine du repo. GitHub ne trouvait pas le workflow.

**Correction :**
```bash
cd ..  # aller à la racine du repo
mkdir .github
mkdir .github\workflows
move projet_accidents\.github\workflows\ci.yml .github\workflows\ci.yml
```

Commit : `ci: move GitHub Actions workflow to repo root`

---

### Étape 6 — Problème : working-directory manquant

**Erreur CI :**
```
Aucun fichier ne correspond à [uv.lock]
```

**Cause :** `uv.lock` et `pyproject.toml` sont dans `projet_accidents/`
mais la CI s'exécutait à la racine du repo.

**Correction :** ajout de `defaults.run.working-directory: projet_accidents`
dans `ci.yml` pour que tous les jobs s'exécutent dans le bon dossier.

Commit : `ci: fix working directory for projet_accidents subfolder`

---

### Étape 7 — Problème : test_api.py mal formatté

**Erreur CI (job lint) :**
```
Would reformat: tests/test_api.py
1 file would be reformatted
```

**Cause :** le fichier de tests n'avait pas été formatté avec ruff.

**Correction :**
```bash
uv run ruff format tests/test_api.py
git add tests/test_api.py
git commit -m "style: format test file with ruff"
```

---

### Étape 8 — Problème avec Vim

En faisant `git merge feature/add-tests`, Git a ouvert Vim pour demander
un message de merge. Vim est un éditeur de texte dans le terminal avec
un fonctionnement particulier — il faut appuyer sur `Echap` puis taper `:q!`
pour sortir sans sauvegarder.

**Solution pour éviter Vim à l'avenir :**
```bash
git config --global core.editor "code --wait"
```

Git ouvrira VS Code à la place.

---

### Résultat final CI

```
✅ lint (ruff check + ruff format)
✅ typecheck (mypy - continue-on-error)
✅ security (bandit - continue-on-error)
✅ tests (4 tests passent)
```

---

### Branches créées en Phase 3

| Branche | Rôle |
|---------|------|
| `feature/add-tests` | Écriture des tests pytest |
| `feature/add-ci-pipeline` | Création du fichier ci.yml |
| `feature/merge-tests` | Merge des tests dans develop via PR |
| `fix/move-ci-to-root` | Déplacement du ci.yml à la racine |
| `fix/ci-working-directory` | Correction du working-directory |
| `fix/format-test-file` | Formatage de test_api.py |

---

## Réponses aux questions de réflexion

### 1. Pourquoi plusieurs jobs séparés ?

**Parallélisme :** les 4 jobs tournent en même temps → CI plus rapide.
Si tout était dans un seul job, il faudrait attendre chaque étape.

**Débogage :** si lint échoue et tests passent, on sait exactement
où est le problème sans lire tous les logs.

### 2. Que faire si la CI échoue ?

**Lire les logs :** sur GitHub → Actions → cliquer sur le job rouge →
développer l'étape qui a échoué → lire le message d'erreur.

**Reproduire localement :**
```bash
uv run ruff check .          # reproduire lint
uv run ruff format --check . # reproduire format check
uv run pytest tests/ -v      # reproduire tests
```

### 3. Faut-il tout corriger d'un coup ?

**Non.** Les petites PR sont meilleures car :
- Plus faciles à relire (10 lignes changées vs 500)
- Si ça casse, on sait exactement quelle correction a causé le problème
- Plus faciles à approuver pour le formateur
- Historique Git plus clair

C'est pourquoi on a créé des branches séparées pour chaque correction.

---

## Résumé Phase 3

| Élément | Statut |
|---------|--------|
| `tests/test_api.py` avec 4 tests | ✅ |
| `.github/workflows/ci.yml` créé | ✅ |
| Job lint (ruff) | ✅ |
| Job typecheck (mypy) | ✅ continue-on-error |
| Job security (bandit) | ✅ continue-on-error |
| Job tests (pytest) | ✅ |
| CI se déclenche sur push/PR | ✅ |
| Cache uv activé | ✅ |

## Ce qui manque encore

- mypy et bandit en mode bloquant (après correction du code)
- Coverage minimum à définir (ex: 80%)
- Ajouter les status checks dans les règles de protection des branches

---

## Réponses complètes aux questions de réflexion

### 1. Pourquoi plusieurs jobs séparés ?

**Avantages du parallélisme :**
Les 4 jobs (lint, typecheck, security, tests) tournent EN MÊME TEMPS
sur des serveurs différents. Si tout était dans un seul job séquentiel :
- lint (30s) → typecheck (30s) → security (30s) → tests (30s) = 2 minutes
Avec 4 jobs parallèles :
- tous tournent en même temps = 30 secondes

**Facilité de débogage :**
Si tu as 4 jobs séparés et que "tests" échoue mais "lint" passe,
tu sais exactement où chercher. Avec un seul job, tu dois lire
200 lignes de logs pour trouver l'erreur.

---

### 2. Que faire si la CI échoue ?

**Comment lire les logs ?**
1. GitHub → Actions → cliquer sur le run rouge
2. Cliquer sur le job qui échoue (ex: "lint")
3. Développer l'étape rouge
4. Lire le message d'erreur

**Comment reproduire localement ?**
```bash
# Reproduire lint
uv run ruff check .
uv run ruff format --check .

# Reproduire les tests
uv run pytest tests/ -v

# Reproduire security
uv run bandit -r app_fastapi.py app.py -ll
```

L'avantage de reproduire localement : tu corriges en 5 secondes
au lieu d'attendre 3 minutes à chaque push.

---

### 3. Faut-il tout corriger d'un coup ?

**Non, jamais.**

**Avantages des petites PR :**
- Plus facile à relire : 10 lignes changées vs 500
- Si ça casse, on sait exactement quelle correction a causé le problème
- Plus facile à approuver pour le formateur
- Historique Git plus clair et lisible

**Facilité de review :**
Une PR qui corrige 1 problème → review en 2 minutes
Une PR qui corrige 50 problèmes → review en 1 heure, risque d'erreurs

C'est pour ça qu'on a créé des branches séparées :
`fix/format-test-file`, `fix/ci-working-directory`, etc.
plutôt que tout mettre dans une seule branche.
