# Veille CI/CD

---

## 📖 Glossaire des termes techniques

Voici les définitions des termes techniques rencontrés tout au long de cette veille.

**Build** : le processus qui transforme le code source en quelque chose d'exécutable ou de déployable. Pour Python, ça peut être : vérifier que le code ne contient pas d'erreurs de syntaxe, lancer les tests, empaqueter le projet en `.whl`... On dit qu'un build "passe" quand tout s'est bien déroulé, et qu'il "échoue" quand une erreur est détectée.

**Pipeline** : une suite d'étapes automatisées qui s'exécutent dans un ordre précis. Un pipeline CI/CD typique ressemble à : 1) récupérer le code → 2) installer les dépendances → 3) lancer le linter → 4) lancer les tests → 5) déployer si tout passe. Chaque étape dépend du succès de la précédente.

**Pull Request (PR)** : une demande de fusion de code sur GitHub. Quand tu travailles sur une branche séparée et que tu veux intégrer tes modifications dans la branche principale (`main`), tu crées une PR. Le CI se déclenche automatiquement pour vérifier que ton code ne casse rien avant la fusion.

**Branche** : une copie parallèle du code dans Git. Tu peux créer une branche `feature/login` pour développer la fonctionnalité de connexion sans toucher au code principal. Quand c'est prêt, tu fusionnes (merge) ta branche dans `main`.

**Merge** : fusionner deux branches Git. Quand plusieurs développeurs travaillent sur des branches différentes et veulent réunir leur travail, ils font un merge. C'est là que les conflits peuvent apparaître si deux personnes ont modifié le même fichier.

**Intégration hell** : l'enfer de l'intégration. Ce qui se passe quand une équipe travaille en silo pendant des semaines, puis essaie de fusionner tout le code en même temps. Le résultat : des dizaines de conflits à résoudre manuellement, des jours perdus. Le CI/CD résout ce problème en forçant des intégrations fréquentes et automatiques.

**Production** : l'environnement réel où tourne l'application et où les vrais utilisateurs interagissent avec elle. S'oppose aux environnements de développement (ton PC) et de staging (environnement de test identique à la prod). Déployer en production = mettre à jour l'application que les utilisateurs utilisent réellement.

**Rollback** : revenir à une version précédente d'une application après qu'un déploiement a causé des problèmes. "Si le déploiement v2.1 plante, on fait un rollback vers v2.0."

**Linter** : outil qui analyse ton code source et signale des erreurs, mauvaises pratiques ou problèmes de style, **sans l'exécuter**. Comme un correcteur orthographique pour le code. Exemples : Ruff, Flake8, Pylint. Voir Mission 4 pour le comparatif complet.

**Formateur (Formatter)** : outil qui réécrit automatiquement ton code pour respecter un style uniforme (indentation, longueur de ligne...). Contrairement au linter qui signale les problèmes, le formateur les corrige seul. Exemples : Black, Ruff Format.

**flake8** : linter Python classique. Vérifie les espaces, les lignes trop longues, les imports inutilisés, les variables non définies. Lancé sur ton code : `flake8 src/`. Retourne des erreurs de type `E501` (ligne trop longue), `F401` (import inutilisé), etc.

**Black** : formateur Python "opinioné" (= qui impose son style sans discussion possible). En passant Black sur ton code, il le reformate automatiquement de façon cohérente. Utilisé par des milliers de projets open source pour éviter les débats "4 espaces vs 2 espaces" en équipe.

**Ruff** : outil moderne écrit en Rust qui combine linter + formateur en un seul outil, 10-100x plus rapide que ses équivalents Python. Remplace Flake8, Black, isort et des dizaines d'autres outils. Voir Mission 4.

**PyPI (Python Package Index)** : le dépôt officiel de packages Python, accessible sur [pypi.org](https://pypi.org). Quand tu fais `pip install pandas` ou `uv add pandas`, le package est téléchargé depuis PyPI. C'est comme un App Store officiel pour Python : n'importe qui peut y publier un package, il en existe plus de 500 000. C'est différent de PyPy (voir ci-dessous).

**PyPy** : *(à ne pas confondre avec PyPI)* une **implémentation alternative** de Python écrite en Python et en C, avec un compilateur JIT (Just-In-Time). L'interpréteur Python standard s'appelle CPython (écrit en C). PyPy peut rendre certains programmes Python 2 à 10x plus rapides grâce à la compilation JIT. Mais pour la plupart des projets Python classiques (data science, web...), CPython + de bonnes pratiques suffit largement. PyPy est surtout utile pour du calcul intensif pur Python.

**Rust** : langage de programmation système connu pour ses performances extrêmes et sa sécurité mémoire. Rust compile directement en code machine (pas d'interpréteur), ce qui le rend aussi rapide que C/C++. uv, Ruff, et d'autres outils Python modernes sont écrits en Rust pour gagner un facteur de vitesse de 10 à 100x par rapport aux équivalents Python.

**Cache** : copie locale de données pour éviter de les retélécharger ou recalculer. Dans le contexte de Python : uv maintient un cache global des packages téléchargés. Si deux projets utilisent la même version de `pandas`, elle n'est téléchargée qu'une fois et partagée. Dans GitHub Actions avec `enable-cache: true`, les dépendances sont mises en cache entre les exécutions du pipeline — si `uv.lock` n'a pas changé, on n'installe rien, on utilise le cache. Résultat : un pipeline qui prend 2 minutes sans cache peut prendre 10 secondes avec cache.

**Cookie** : fichier texte stocké par ton navigateur, déposé par un site web pour se souvenir de toi. Exemple : quand tu te connectes à GitHub, un cookie garde ta session active. Sans cookie, tu devrais rentrer ton mot de passe à chaque page. N'a rien à voir avec le cache du code.

**Lockfile (uv.lock, poetry.lock)** : fichier qui "fige" les versions exactes de toutes les dépendances. Quand tu fais `uv add pandas`, uv installe la dernière version de pandas ET toutes ses dépendances transitives (numpy, pytz, etc.) et note leurs versions exactes dans `uv.lock`. Résultat : quand un collègue clone le projet et fait `uv sync`, il obtient exactement les mêmes versions. "Fonctionne sur mon ordi" disparaît.

**Dépendance directe** : un package que tu installes toi-même volontairement. Exemple : `uv add fastapi`.

**Dépendance transitive** : un package installé automatiquement parce qu'il est nécessaire à une de tes dépendances directes. Exemple : FastAPI dépend de Starlette et Pydantic — ces packages sont installés automatiquement même si tu ne les as pas demandés. Tu demandes 1 package, tu en obtiens 4-5.

**Wheel (.whl)** : format de distribution d'un package Python, prêt à installer. C'est l'équivalent d'un `.exe` pour Windows mais pour Python. Quand tu publies un package sur PyPI, tu crées un wheel que les gens peuvent installer avec pip. Le wheel contient le code compilé et les métadonnées, donc l'installation est plus rapide qu'une source distribution qui nécessite une compilation.

**Python pur** : code Python qui ne contient pas d'extensions en C ou C++ (modules natifs). La plupart du code Python est "pur Python". Numpy par exemple n'est pas pur Python — il contient des extensions C pour la performance. Le build backend de uv ne supporte que le Python pur.

**Environnement virtuel (venv)** : dossier isolé qui contient une installation Python et des packages indépendante du reste du système. Sans venv, tous tes projets partagent la même installation Python, ce qui cause des conflits de versions ("le projet A nécessite Django 3.2, le projet B nécessite Django 4.1"). Avec un venv par projet, chacun a ses propres packages.

**YAML** : format de fichier de configuration lisible par les humains, utilisé par GitHub Actions, Docker Compose, Kubernetes... La syntaxe repose sur l'indentation (comme Python). `.yml` et `.yaml` sont la même chose.

**Workflow GitHub Actions** : fichier YAML dans `.github/workflows/` qui définit quand et comment exécuter des actions automatisées (tests, déploiement...). Se déclenche sur des événements GitHub (push, pull request...).

**Job** : une unité de travail dans un workflow GitHub Actions. Un workflow peut contenir plusieurs jobs qui s'exécutent en parallèle ou séquentiellement.

**Step** : une étape dans un job. Chaque `- uses:` ou `- run:` dans un workflow est un step.

**Runner** : la machine virtuelle GitHub sur laquelle s'exécute un workflow. `runs-on: ubuntu-latest` indique qu'on veut une VM Ubuntu. GitHub en fournit des gratuits pour les dépôts publics.

**Webhook** : mécanisme où un service (GitHub) envoie automatiquement une requête HTTP à un autre service quand un événement se produit. Quand tu fais un push sur GitHub, GitHub envoie un webhook aux services configurés (comme un service CI externe) pour les notifier.

**Versionnage sémantique (SemVer)** : convention de numérotation des versions sous la forme `MAJEUR.MINEUR.PATCH`. Voir Mission 3 pour les détails.

**Tag Git** : une étiquette sur un commit Git, généralement pour marquer une version (`v1.2.0`). Contrairement à une branche qui avance au fur et à mesure des commits, un tag pointe toujours vers le même commit.

**CHANGELOG** : fichier qui liste tous les changements entre chaque version d'un projet. Généré automatiquement par python-semantic-release à partir des commits conventionnels.

**Release GitHub** : une page sur GitHub associée à un tag Git, qui résume les changements de cette version et peut inclure des fichiers à télécharger (binaires, wheels...). python-semantic-release crée ces releases automatiquement.

**Docstring** : commentaire en triple guillemets dans une fonction Python, qui documente ce que fait la fonction, ses paramètres et ce qu'elle retourne. C'est le standard Python pour la documentation de code, et mkdocstrings les lit pour générer de la documentation automatiquement.

**Site statique** : site web dont les fichiers HTML/CSS/JS sont générés une fois et servis tels quels, sans base de données ni calcul côté serveur à chaque visite. MkDocs génère un site statique : rapide, sécurisé, hébergeable gratuitement sur GitHub Pages.

**Markdown** : langage de balisage léger pour formater du texte. `**gras**` → **gras**, `# Titre` → titre, `` `code` `` → `code`. Les fichiers `.md` sont écrits en Markdown. C'est le format utilisé pour les README, la documentation MkDocs, et ce fichier même.

---

# Mission 1 : Comprendre CI/CD

## Qu'est-ce que la CI (Intégration Continue) ?

La CI (Intégration Continue) cherche à automatiser les opérations autour du développement. Elle permet de vérifier automatiquement le code à chaque modification.

### Quels problèmes résout-elle ?

- Détecter les bugs **avant** qu'ils arrivent en production
- Détecter le code incompatible : s'assurer que le nouveau code s'intègre bien
- Réduire l'**intégration hell** : éviter les conflits quand plusieurs devs fusionnent leur code après des semaines de travail isolé
- Réduire le temps passé à résoudre les conflits de merge
- Réduire les coûts liés aux bugs

### Quels sont les principes clés ?

- **Commits fréquents** : les développeurs poussent leur code au moins une fois par jour
- **Tests automatisés** : chaque commit déclenche une suite de tests automatiques
- **Build automatique** : le code est compilé/construit automatiquement à chaque push
- **Feedback rapide** : les développeurs sont informés immédiatement si le code casse quelque chose
- **Un seul dépôt principal** : tout le monde travaille sur la même branche
- **Correction immédiate** : si le build échoue, la priorité est de résoudre le problème

### 3 exemples d'outils de CI

- GitHub Actions
- Jenkins
- GitLab CI/CD

---

## Qu'est-ce que le CD (Continuous Deployment/Delivery) ?

La CD (Déploiement Continu), qui prolonge la CI, cherche à automatiser les opérations de déploiement. En d'autres termes, c'est le fait de mettre automatiquement en ligne l'application validée.

Il existe 2 variantes :

- **Continuous Delivery** : le code est prêt à être déployé, mais le déclenchement reste manuel (semi-automatique, pour décider du timing)
- **Continuous Deployment** : le code est déployé automatiquement en production (100% automatique)

### Différence entre Livraison Continue et Déploiement Continu

| | Continuous Delivery | Continuous Deployment |
|---|---|---|
| Déclenchement | Manuel (après validation) | Automatique |
| Fréquence | Selon les besoins business | Plusieurs fois par jour |
| Intervention humaine | Oui | Non |

### Quels sont les risques et les bénéfices ?

**Risques :**

- **Bugs en production** : un bug non détecté peut affecter les utilisateurs rapidement
- **Dépendance aux tests** : si les tests ne couvrent pas bien le code, des erreurs peuvent passer
- **Complexité technique** : nécessite une infrastructure robuste et des rollbacks (retour à la version précédente) rapides
- **Résistance au changement** : les équipes habituées aux releases mensuelles peuvent être réticentes
- **Monitoring critique** : besoin de surveillance constante pour détecter les problèmes rapidement

**Bénéfices :**

- **Time-to-market réduit** : les fonctionnalités arrivent plus vite aux utilisateurs
- **Feedback utilisateur rapide** : on peut tester les hypothèses business rapidement
- **Moins de stress** : les déploiements fréquents sont moins risqués que les grosses releases
- **Correction rapide** : un bug détecté peut être corrigé et déployé en quelques heures
- **Amélioration continue** : les petits changements sont plus faciles à débugger
- **Réduction des coûts** : moins de temps passé en réunions de coordination de releases

---

## Pourquoi le CI/CD est-il important ?

**Impact sur la qualité du code :**

- **Détection précoce des bugs** : les tests automatiques tournent à chaque commit, les erreurs sont détectées en minutes au lieu de jours
- **Code review facilité** : les petits commits fréquents sont plus faciles à reviewer que 1000 lignes d'un coup
- **Standards de code maintenus** : les linters et formateurs automatiques s'exécutent automatiquement
  - `flake8` : linter Python qui vérifie les espaces, les lignes trop longues, les imports inutiles, etc.
  - `Black` : formateur Python qui corrige automatiquement le code
- **Régression évitée** : détecte quand du code qui fonctionnait avant se met à casser

**Impact sur la vitesse de développement :**

- **Livraison accélérée** : de plusieurs semaines/mois entre chaque release à plusieurs déploiements par jour (ex : Netflix déploie des milliers de fois par jour)
- **Moins de temps perdu** : plus de journées entières à résoudre des conflits de merge
- **Feedback loop rapide** : les devs voient immédiatement si leur code fonctionne
- **Réduction du time-to-market** : avantage concurrentiel important si une idée peut aller du concept à la prod en quelques jours au lieu de mois

**Impact sur la collaboration en équipe :**

- **Transparence totale** : tout le monde voit l'état du build, les tests qui passent/échouent — moins de "ça ne marche que sur mon ordi"
- **Responsabilité partagée** : quand le build casse, toute l'équipe s'implique pour le réparer rapidement
- **Moins de silos** : quand chaque équipe travaille isolée sans parler aux autres → avec CI/CD, devs + testeurs + ops = **DevOps** (communication fluide, responsabilités partagées, problèmes résolus plus vite)
- **Onboarding facilité** : le processus est documenté et automatisé, une nouvelle personne peut rejoindre l'équipe plus facilement

> 💡 **En résumé** : le CI/CD transforme le développement logiciel d'un processus manuel et risqué en une chaîne automatisée et fiable. C'est une compétence très demandée, notamment en ML/AI où il sert à automatiser le réentraînement des modèles et les pipelines de données.

---

## Exemple de workflow CI/CD

```yaml
name: CI/CD Chatbot RAG

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### Décryptage ligne par ligne

**`name: CI/CD Chatbot RAG`**
Juste un nom pour identifier ce workflow dans GitHub Actions.

**`on: push: branches: [main]`**
QUAND ce script s'exécute : quand quelqu'un envoie du code sur la branche `main`.

**`on: pull_request: branches: [main]`**
OU quand quelqu'un crée une "pull request" vers `main` (= demander à ce que son code soit fusionné dans le projet).

**`runs-on: ubuntu-latest`**
GitHub crée un **ordinateur virtuel temporaire** avec Ubuntu (système Linux, gratuit et très utilisé sur les serveurs).

- Peu importe l'OS utilisé (Windows/Mac), les tests tournent toujours sur Ubuntu
- Environnement propre et identique pour tout le monde
- L'ordi virtuel est supprimé automatiquement après

> 💡 En résumé : GitHub crée un ordi virtuel, installe Ubuntu, fait tourner les tests, puis supprime l'ordi. **TOUT ÇA AUTOMATIQUEMENT !**

---

# Mission 2 : Maîtriser uv

## Qu'est-ce que uv ?

uv est un **gestionnaire de paquets et de projets Python ultra-rapide**, écrit en Rust et développé par Astral (les créateurs de Ruff). Il a été conçu pour remplacer en un seul outil tous les outils éparpillés de l'écosystème Python.

uv est **10 à 100x plus rapide que pip** grâce à son architecture en Rust.

**uv remplace tous ces outils en un seul :**

- `pip` (installation de paquets)
- `pip-tools` (compilation de requirements)
- `pipx` (exécution d'outils isolés)
- `poetry` / `rye` (gestion de projets)
- `pyenv` (gestion des versions Python)
- `virtualenv` / `venv` (environnements virtuels)
- `twine` (publication sur PyPI)

---

## En quoi est-ce différent de pip / poetry / pipenv ?

| Fonctionnalité | pip | poetry | pipenv | uv |
|---|---|---|---|---|
| Vitesse | Lent | Moyen | Lent | 10-100x plus rapide |
| Gestion de projet | Non | Oui | Partiel | Oui (complet) |
| Lockfile | Non | poetry.lock | Pipfile.lock | uv.lock |
| Versions Python | Non | Non | Partiel | Oui (intégré) |
| Un seul outil | Non | Non | Non | Oui |
| Compatible pip | Natif | Non | Non | Interface uv pip |
| Langage | Python | Python | Python | Rust |
| Installation sans Python | Non | Non | Non | Oui |

---

## Quels sont les avantages ?

**Performance**

La vitesse est le point le plus frappant. Là où pip peut prendre 30 secondes pour installer un ensemble de dépendances, uv le fait en moins d'une seconde grâce à :

- **Résolution de dépendances parallélisée** : quand tu télécharges pandas, pandas a lui-même besoin d'autres packages (numpy, etc.). pip les télécharge un par un. uv les télécharge tous en même temps.
- **Compilation Rust** : pip est écrit en Python, uv est écrit en Rust — un langage qui compile directement en code machine ultra-rapide, sans intermédiaire.
- **Lockfile binaire ultra-efficace** : le fichier `uv.lock` note exactement quelle version de chaque package est utilisée. Quand quelqu'un clone le projet, uv lit ce fichier et installe exactement les mêmes versions — tout le monde a le même environnement, sans surprise.
- **Cache global dédupliquant les téléchargements** : si 2 projets utilisent la même version de numpy, elle n'est téléchargée et stockée qu'une seule fois. Économie d'espace disque et de temps.

**Outil unique**

Avant uv, un workflow typique nécessitait : pyenv + virtualenv + pip + pip-tools + pipx. Avec uv, une seule commande gère tout cela.

**Reproductibilité**

Le fichier `uv.lock` contient les versions exactes de TOUTES les dépendances :
- **Directes** : ce que tu installes toi-même volontairement (ex : `uv add pandas`)
- **Transitives** : ce que pandas a besoin pour fonctionner mais que tu n'as pas demandé — tu demandes 1 package, uv en installe 4 automatiquement

Commité dans le dépôt, ce fichier garantit que tous les devs et la CI/CD ont exactement le même environnement.

**Installation sans prérequis**

uv s'installe via un simple script curl ou powershell. Pas besoin d'avoir Python déjà installé sur la machine.

---

## Commandes essentielles

```bash
# Installation de uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Créer un nouveau projet
uv init mon-projet
cd mon-projet

# Ajouter une dépendance de production
uv add requests
uv add pandas numpy

# Ajouter une dépendance de dev
uv add --dev pytest ruff

# Installer toutes les dépendances
uv sync

# Lancer un script/commande dans l'environnement
uv run python main.py
uv run pytest

# Installer/gérer Python
uv python install 3.12
uv python pin 3.11
```

---

## Comment uv fonctionne avec pyproject.toml ?

Le fichier `pyproject.toml` est le **fichier de configuration central** d'un projet uv. Il remplace `requirements.txt`, `setup.py`, `setup.cfg` et tous les autres fichiers de configuration fragmentés. C'est la source de vérité unique pour ton projet.

### Structure complète du fichier

```toml
# ----------------------------------------
# SECTION 1 : Métadonnées du projet (PEP 621)
# ----------------------------------------
[project]
name = "mon-projet"
version = "0.1.0"
description = "Description de mon projet"
readme = "README.md"
requires-python = ">=3.11"

# Dépendances de PRODUCTION (installées chez les utilisateurs)
dependencies = [
    "requests>=2.28.0",
    "pandas>=2.0.0",
    "fastapi>=0.100.0",
]

# Extras (dépendances optionnelles)
[project.optional-dependencies]
ml = ["scikit-learn>=1.3", "torch>=2.0"]
viz = ["matplotlib>=3.7", "plotly>=5.0"]

# ----------------------------------------
# SECTION 2 : Dépendances de DÉVELOPPEMENT
# ----------------------------------------
[dependency-groups]
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
test = [
    "pytest-cov>=4.0",
    "httpx>=0.24.0",
]

# ----------------------------------------
# SECTION 3 : Build backend
# ----------------------------------------
[build-system]
requires = ["uv_build>=0.10.4,<0.11.0"]
build-backend = "uv_build"

# ----------------------------------------
# SECTION 4 : Configuration uv spécifique
# ----------------------------------------
[tool.uv]
package = true  # true = librairie publiable, false = app simple

[tool.uv.sources]
mon-autre-lib = { path = "../mon-autre-lib", editable = true }

[tool.uv.build-backend]
module-root = ""
module-name = "mon_projet"
```

---

### Gestion des dépendances par sections

**Dépendances de production : `[project.dependencies]`**

Ce sont les dépendances nécessaires à l'exécution de l'application. Elles sont installées quand quelqu'un installe ton paquet depuis PyPI.

```toml
[project]
dependencies = [
    "requests>=2.28.0",       # version minimale requise
    "pandas>=2.0.0,<3.0.0",   # contrainte de version
    "numpy",                   # sans contrainte (déconseillé)
    "fastapi>=0.100.0",
]
```

**Dépendances de développement : `[dependency-groups]`**

Ces dépendances ne sont **pas installées** chez les utilisateurs finaux. Elles servent uniquement en développement (tests, linting, formatage).

```toml
[dependency-groups]
# Groupe 'dev' : installé par défaut avec uv sync
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

# Groupe personnalisé 'test'
test = [
    "pytest-cov>=4.0",
    "faker>=18.0",
]
```

Commandes associées :

```bash
uv add --dev pytest           # ajoute dans [dependency-groups.dev]
uv add --group test faker     # ajoute dans [dependency-groups.test]
uv sync                       # installe tout (prod + dev)
uv sync --no-dev              # installe seulement la prod
uv sync --group test          # installe prod + groupe test
```

**Dépendances optionnelles (extras) : `[project.optional-dependencies]`**

Les extras sont des fonctionnalités optionnelles que les utilisateurs peuvent installer. Elles apparaissent sur PyPI.

```toml
[project.optional-dependencies]
ml = ["scikit-learn>=1.3", "xgboost>=2.0"]
viz = ["matplotlib>=3.7", "plotly>=5.0"]

# Installation par les utilisateurs :
# pip install mon-projet[ml]
# pip install mon-projet[ml,viz]
```

**Différence clé entre `dependency-groups` et `optional-dependencies` :**

| Caractéristique | dependency-groups | optional-dependencies |
|---|---|---|
| Publiées sur PyPI | Non | Oui |
| Utilisées par | Développeurs du projet | Utilisateurs finaux |
| Exemples typiques | pytest, ruff, mypy | scikit-learn pour [ml] |
| Installée avec uv sync | Oui (--dev ou --group) | Non par défaut |

---

### Créer un backend avec uv

Le build backend uv permet de transformer un projet en **paquet distribuable** (wheel ou source distribution). Il ne supporte que le Python pur (pas d'extensions C).

> 💡 **Paquet distribuable** = empaqueter ton projet pour que quelqu'un puisse l'installer avec `pip install`. C'est comme créer un `.exe` sur Windows, sauf que c'est pour Python. Le format `.whl` (wheel) est l'extension des paquets Python prêts à installer.

**Structure de dossier recommandée (layout src)**

```
mon-projet/
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── mon_projet/
        ├── __init__.py
        └── main.py
```

**Configuration du build backend**

```toml
[build-system]
requires = ["uv_build>=0.10.4,<0.11.0"]
build-backend = "uv_build"

# Configuration optionnelle
[tool.uv.build-backend]
module-root = "src"       # dossier contenant le module (défaut: "src")
module-name = "mon_projet" # nom du module (défaut: dérivé du nom du projet)
```

> 💡 Le build backend uv est inclus dans uv lui-même. Lors d'un `uv build`, uv utilise sa copie intégrée du backend si elle est compatible, ce qui rend les builds encore plus rapides.

**Commandes de build**

```bash
# Construire wheel + source distribution
uv build

# Publier sur PyPI
uv publish

# Publier sur un registre privé
uv publish --publish-url https://mon-registre.com/simple/
```

---

## Comment utiliser uv dans GitHub Actions ?

L'utilisation de uv dans GitHub Actions présente plusieurs avantages :

- Installations de dépendances 10-100x plus rapides = pipelines CI/CD qui se terminent en secondes
- Cache des dépendances intégré et facile à configurer
- Reproductibilité parfaite grâce au `uv.lock`
- Action officielle `setup-uv` simple et bien maintenue
- Gestion automatique de la version Python

### Méthode 1 : setup-uv (recommandée)

C'est l'action officielle créée par Astral (les créateurs d'uv). Elle installe uv sur la machine virtuelle GitHub.

```yaml
# .github/workflows/ci.yml

name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: '0.5.0'     # optionnel, défaut : dernière version
          enable-cache: true   # active le cache GitHub Actions

      - name: Set up Python
        run: uv python install 3.12
```

En résumé :

```yaml
- uses: astral-sh/setup-uv@v4   # installe uv
- run: uv sync                   # installe les dépendances
- run: uv run pytest             # lance les tests
```

### Méthode 2 : Python matrix

Permet de tester le code sur **plusieurs versions de Python en même temps** (ex : 3.10, 3.11 et 3.12). GitHub lance 3 pipelines en parallèle, un pour chaque version. Utile si tu crées une librairie utilisée avec des versions Python différentes.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4

      - name: Install uv and set Python version
        uses: astral-sh/setup-uv@v4
        with:
          python-version: ${{ matrix.python-version }}
          enable-cache: true
```

### Cache des dépendances

Le cache est la clé pour des pipelines rapides. `setup-uv` intègre automatiquement le cache GitHub Actions quand `enable-cache` est activé.

> 💡 **Cache** = les dépendances sont mémorisées sur les serveurs GitHub pour ne pas être retéléchargées à chaque push. Le cache se régénère uniquement quand `uv.lock` change.

```yaml
# Cache simple
- name: Install uv with cache
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
    # La clé de cache est automatiquement basée sur uv.lock

# Cache avancé avec suffixe (utile si plusieurs jobs avec des deps différentes)
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
    cache-suffix: 'test'   # distingue les caches par job
```

### Workflow CI/CD complet

```yaml
name: CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
          python-version: '3.12'

      - name: Install dependencies
        run: uv sync --all-groups

      - name: Lint with ruff
        run: |
          uv run ruff check src/
          uv run ruff format --check src/

      - name: Type check
        run: uv run mypy src/

      - name: Run tests
        run: uv run pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml

  publish:
    runs-on: ubuntu-latest
    needs: lint-and-test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        run: uv publish
        env:
          UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

### Bonnes pratiques

| Pratique | Description | Commande/Config |
|---|---|---|
| Toujours committer uv.lock | Garantit la reproductibilité exacte | `git add uv.lock` |
| Activer le cache | Réduit drastiquement le temps de build | `enable-cache: true` |
| Utiliser uv run | Exécute dans le venv sans l'activer | `uv run pytest` |
| Fixer la version de uv | Évite les surprises avec les mises à jour | `version: '0.5.0'` |
| --no-dev en prod | N'installe pas les outils de dev en prod | `uv sync --no-dev` |
| Cache-suffix par job | Évite les conflits de cache entre jobs | `cache-suffix: 'test'` |

---

# Mission 3 : Semantic Release

## 1. Le versionnage sémantique (SemVer)

Le versionnage sémantique est une convention pour numéroter les versions d'un logiciel de façon lisible et prévisible.

**Format : `MAJEUR.MINEUR.PATCH`**

Exemple : `2.4.1`
- `2` = version majeure
- `4` = version mineure
- `1` = patch

**Quand bumper chaque niveau ?**

| Niveau | Quand ? | Exemple |
|---|---|---|
| PATCH | Correction de bug, rien ne casse | `1.0.0` → `1.0.1` |
| MINOR | Nouvelle fonctionnalité, compatible avec l'ancienne version | `1.0.0` → `1.1.0` |
| MAJOR | Changement qui casse la compatibilité | `1.0.0` → `2.0.0` |

> 💡 Exemple concret : si tu utilises pandas 1.5.0 et que pandas sort la version 1.6.0, tu peux mettre à jour sans rien casser (MINOR). Si pandas sort la version 2.0.0, méfie-toi, des choses peuvent casser (MAJOR).

---

## 2. Conventional Commits

C'est une convention qui impose un format précis pour les messages de commit Git. L'objectif : que les outils puissent lire les commits et décider automatiquement quelle version bumper.

**Format des messages**

```
<type>[étendue optionnelle]: <description courte>

[corps optionnel]

[pied optionnel]
```

**Exemples concrets**

```bash
feat: ajout de la connexion utilisateur
fix: correction du bug d'affichage du tableau de bord
docs: mise à jour du README
feat(api)!: refonte complète des endpoints
```

**Types de commits**

| Type | Description | Impact sur la version |
|---|---|---|
| `feat` | Nouvelle fonctionnalité | → MINOR (`1.1.0`) |
| `fix` | Correction de bug | → PATCH (`1.0.1`) |
| `docs` | Documentation uniquement | Aucun |
| `style` | Formatage, espaces (pas de logique) | Aucun |
| `refactor` | Réécriture sans nouvelle fonctionnalité | Aucun |
| `test` | Ajout ou modification de tests | Aucun |
| `chore` | Maintenance, mise à jour de dépendances | Aucun |
| `BREAKING CHANGE` | Rupture de compatibilité (ajout de `!`) | → MAJOR (`2.0.0`) |

**Impact sur le versionnage**

```
fix: correction bug login       → 1.0.0 devient 1.0.1
feat: ajout export PDF          → 1.0.1 devient 1.1.0
feat!: refonte API complète     → 1.1.0 devient 2.0.0
```

---

## 3. Python Semantic Release

`python-semantic-release` est un outil qui lit automatiquement les commits, décide quelle version bumper, génère le CHANGELOG et crée la release GitHub — tout ça automatiquement.

**Fonctionnement en résumé**

```
commits → PSR les lit → bumpe la version → génère CHANGELOG → crée release GitHub
```

**Configuration dans pyproject.toml**

```toml
[tool.semantic_release]
commit_parser = "conventional"
version_toml = ["pyproject.toml:project.version"]

[tool.semantic_release.changelog.default_templates]
changelog_file = "CHANGELOG.md"
```

**Génération du CHANGELOG**

Le CHANGELOG est un fichier qui liste tous les changements de chaque version. PSR le génère automatiquement à partir des commits.

Exemple de CHANGELOG généré :

```markdown
## v1.2.0 (2025-02-20)
### Features
- ajout de l'export PDF (#42)
- nouvelle page de profil utilisateur (#38)

## v1.1.1 (2025-02-10)
### Bug Fixes
- correction du bug d'affichage mobile (#35)
```

**Création des releases GitHub**

PSR exécute automatiquement ces étapes dans cet ordre :

1. Lit tous les commits depuis la dernière release
2. Détermine la nouvelle version (`fix` → PATCH, `feat` → MINOR, `!` → MAJOR)
3. Met à jour le numéro de version dans `pyproject.toml`
4. Génère le `CHANGELOG.md`
5. Crée un commit avec ces changements
6. Crée un tag Git (`v1.2.0`)
7. Pousse sur GitHub et crée une Release GitHub officielle

**Workflow GitHub Actions avec PSR**

```yaml
name: Release
on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # récupère tout l'historique des commits

      - uses: astral-sh/setup-uv@v4

      - name: Run semantic-release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          uvx python-semantic-release version
          uvx python-semantic-release publish
```

> 💡 `fetch-depth: 0` est obligatoire : sans ça, PSR ne voit que le dernier commit et ne peut pas calculer la version correctement.

---

# Mission 5 : MkDocs et GitHub Pages

## 1. Comment MkDocs génère de la documentation ?

**Source : [mkdocs.org](https://www.mkdocs.org)**

MkDocs est un générateur de site statique conçu spécifiquement pour la documentation de projets. Tu écris ta doc en Markdown, tu configures un seul fichier YAML, et MkDocs génère un site HTML complet prêt à être hébergé.

```
fichiers .md + mkdocs.yml  →  MkDocs  →  site HTML statique
```

**Structure d'un projet MkDocs**

```
mon-projet/
├── mkdocs.yml       # fichier de configuration
└── docs/
    ├── index.md     # page d'accueil
    ├── installation.md
    └── api.md
```

**Fichier mkdocs.yml minimal**

```yaml
site_name: Mon Projet
nav:
  - Accueil: index.md
  - Installation: installation.md
  - API Reference: api.md
```

**Commandes essentielles**

```bash
# Installer MkDocs
pip install mkdocs

# Lancer un serveur local avec rechargement automatique
mkdocs serve
# → prévisualisation sur http://127.0.0.1:8000

# Construire le site HTML statique
mkdocs build
# → génère un dossier site/
```

> 💡 Le serveur local se recharge automatiquement à chaque sauvegarde : tu vois le résultat en temps réel pendant que tu écris.

---

## 2. Material for MkDocs

**Source : [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material)**

Material for MkDocs est le thème le plus populaire pour MkDocs. Il transforme la documentation en un site professionnel moderne sans aucune connaissance en HTML/CSS.

**Fonctionnalités clés :**

- Recherche intégrée dans le navigateur (fonctionne même hors ligne)
- Responsive : s'adapte automatiquement mobile/tablette/desktop
- Plus de 10 000 icônes et emojis disponibles
- Annotations de code enrichies
- Disponible en 60+ langues
- Utilisé par des projets majeurs : FastAPI, Typer, SQLModel

**Installation et configuration**

```bash
pip install mkdocs-material
```

```yaml
# mkdocs.yml
site_name: Mon Projet
theme:
  name: material
  language: fr
  palette:
    primary: blue
```

---

## 3. Déployer sur GitHub Pages

**Source : [docs.github.com/fr/pages](https://docs.github.com/fr/pages)**

GitHub Pages est un service d'hébergement **gratuit** de GitHub qui publie un site statique directement depuis un dépôt GitHub. L'URL générée est : `https://ton-username.github.io/ton-repo/`

**Déploiement manuel (une commande)**

```bash
mkdocs gh-deploy
```

MkDocs construit le site et le pousse automatiquement sur la branche `gh-pages` du dépôt. GitHub Pages sert ensuite cette branche publiquement.

**Déploiement automatique via GitHub Actions**

À chaque push sur `main`, la doc se reconstruit et se redéploie automatiquement :

```yaml
name: Deploy Documentation
on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install mkdocs mkdocs-material

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
```

> 💡 GitHub Pages peut publier depuis un workflow GitHub Actions personnalisé, pas seulement depuis une branche. C'est ce qu'on fait ici avec `gh-deploy --force`.

---

## 4. Qu'est-ce que mkdocstrings ?

`mkdocstrings` est un plugin MkDocs qui génère automatiquement la documentation du code Python à partir des **docstrings** (commentaires en triple guillemets dans les fonctions).

**Sans mkdocstrings** → tu réécris manuellement la documentation de chaque fonction.

**Avec mkdocstrings** → tu mets un commentaire dans ton code, et la doc se génère toute seule.

**Exemple**

Ton code Python :

```python
def calculer_moyenne(notes: list[float]) -> float:
    """
    Calcule la moyenne d'une liste de notes.

    Args:
        notes: Liste des notes.

    Returns:
        La moyenne des notes.
    """
    return sum(notes) / len(notes)
```

Dans le fichier `docs/api.md`, tu écris juste :

```markdown
## Référence API

::: mon_module.calculer_moyenne
```

MkDocs génère automatiquement une page complète avec les paramètres, types et description.

**Installation**

```bash
pip install mkdocstrings[python]
```

```yaml
# mkdocs.yml
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
```

> 💡 **Résumé** : MkDocs transforme le Markdown en site web → Material le rend beau → mkdocstrings génère la doc depuis le code → GitHub Pages héberge tout ça gratuitement.
