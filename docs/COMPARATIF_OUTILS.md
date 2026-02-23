# Mission 4 : Comparatif d'outils CI/CD

---

## Glossaire des termes techniques

Avant de plonger dans les comparatifs, voici les définitions des termes techniques qui reviennent souvent.

**Linter** : un outil qui lit ton code source et signale des erreurs, des mauvaises pratiques ou des problèmes de style **sans exécuter le code**. C'est comme un correcteur orthographique, mais pour le code. Il ne corrige pas tout seul, il te dit où il y a un problème.

**Formateur / Formatter** : un outil qui **réécrit automatiquement** ton code pour qu'il respecte un style uniforme (indentation, longueur de ligne, guillemets...). Contrairement au linter qui te signale les problèmes, le formateur les corrige tout seul.

**Type checker (vérificateur de types)** : Python est un langage à typage dynamique — tu peux écrire `x = 5` puis `x = "bonjour"` sans erreur. Mais tu peux aussi ajouter des **annotations de types** dans ton code (`def ma_fonction(x: int) -> str:`). Un type checker lit ces annotations et vérifie que tu ne passes pas un `string` là où tu avais dit que tu attendais un `int`. C'est détecté **avant d'exécuter** le programme.

**AST (Abstract Syntax Tree)** : quand Python lit ton code, il le transforme en une structure arborescente qui représente la logique du programme. Les linters et scanners de sécurité parcourent cet arbre pour détecter des patterns dangereux. C'est pour ça qu'ils peuvent analyser le code sans l'exécuter.

**Analyse statique** : analyser le code sans l'exécuter. S'oppose à l'**analyse dynamique** qui exécute le programme pour observer son comportement.

**CVE (Common Vulnerabilities and Exposures)** : base de données mondiale des failles de sécurité connues. Chaque faille reçoit un identifiant unique (ex: `CVE-2023-12345`). Les scanners comparent tes dépendances à cette liste pour détecter si tu utilises une version vulnérable.

**SAST (Static Application Security Testing)** : test de sécurité basé sur l'analyse statique du code source, sans l'exécuter. C'est ce que fait Bandit par exemple.

**SCA (Software Composition Analysis)** : analyse des dépendances (les packages que tu installes) pour détecter des vulnérabilités connues. C'est ce que fait Safety ou Trivy.

**Faux positif** : une alerte de sécurité levée par un outil alors que le code n'est **pas réellement** vulnérable. Trop de faux positifs = les développeurs ignorent toutes les alertes (le "cry wolf" de la sécurité).

**PyPI (Python Package Index)** : le dépôt officiel de packages Python. Quand tu fais `pip install pandas`, il télécharge depuis pypi.org. C'est comme un App Store officiel pour Python, ouvert à tout le monde. N'importe qui peut y publier un package, d'où l'importance de scanner les dépendances pour les vulnérabilités.

**Rust** : langage de programmation système (comme C++) connu pour ses performances extrêmes et sa sécurité mémoire. Ruff et uv sont écrits en Rust, ce qui explique pourquoi ils sont 10 à 100x plus rapides que leurs équivalents écrits en Python.

---

## 🎨 1. Linters Python

> 💡 **Rappel** : un linter analyse le code sans l'exécuter et signale les problèmes. Il ne les corrige pas (sauf mention contraire).

### Les 3 outils

**Ruff** — sorti en 2022, écrit en Rust par Astral (les créateurs de uv). Il réimplémente les règles de Flake8, Pylint, isort et des dizaines de plugins en un seul outil ultra-rapide. Plus de 800 règles intégrées.

**Flake8** — sorti en 2010, écrit en Python. Le linter "classique" de référence pendant 10+ ans. Fonctionne via un système de plugins pour étendre ses règles.

**Pylint** — sorti en 2003, écrit en Python. Le plus complet : il fait de l'inférence de types, vérifie le nombre d'arguments dans les appels de fonction, contrôle les conventions de nommage, génère un score de qualité... mais c'est le plus lent.

### Comparatif

| Critère | Ruff | Flake8 | Pylint |
|---|---|---|---|
| **Vitesse** | ⚡ 10-100x plus rapide | 🐢 Moyen | 🐌 Lent (2-5 min sur gros projet) |
| **Nombre de règles** | 800+ | ~300 (+ plugins) | ~409 (mais très approfondies) |
| **Auto-correction** | ✅ Oui (`ruff --fix`) | ❌ Non | ❌ Non |
| **Plugins tiers** | ❌ Non (tout intégré) | ✅ Oui (extensible) | ✅ Oui |
| **Inférence de types** | ❌ Non | ❌ Non | ✅ Oui |
| **Config unique** | ✅ pyproject.toml | ✅ setup.cfg / tox.ini | ✅ .pylintrc |
| **Langage** | Rust | Python | Python |
| **Score de qualité** | ❌ Non | ❌ Non | ✅ Oui (note /10) |
| **Adoption** | 🚀 En forte croissance | 🏆 Standard historique | 📉 En déclin |

### Benchmark de vitesse réel

Sur un projet de **120 000 lignes de code Python** :

| Outil | Temps d'exécution |
|---|---|
| Pylint | ~2 minutes 30 |
| Flake8 | ~20 secondes |
| Ruff | **0,4 seconde** |

> Source : retours de l'équipe Dagster. "Sur notre plus grand module (250k LOC), Pylint prend 2,5 minutes avec 4 cœurs. Ruff analyse tout le dépôt en 0,4 secondes."

### Justification du choix

✅ **Choix : Ruff**

Ruff s'impose comme le choix évident en 2024 pour les nouveaux projets. Sa vitesse est tellement supérieure qu'elle change l'expérience de développement : assez rapide pour être lancé en pre-commit hook (à chaque commit), là où Pylint rend la chose impraticable. Il couvre déjà 800+ règles incluant les meilleures de Flake8 et une partie de Pylint, et peut corriger automatiquement les problèmes qu'il détecte.

La seule raison de garder Pylint est si on a besoin de son inférence de types poussée ou de plugins très spécifiques à un framework (ex: Pylint-Django). Dans ce cas, on peut combiner : Ruff en pre-commit pour la vitesse, Pylint en CI pour la profondeur.

---

## 🎨 2. Formateurs Python

> 💡 **Rappel** : un formateur réécrit ton code automatiquement. Tu n'as pas à corriger manuellement les problèmes de style.

### Les 3 outils

**Ruff Format** — le formateur intégré à Ruff, compatible avec le style Black. Écrit en Rust, ultra-rapide, même outil que le linter.

**Black** — "The uncompromising Python code formatter". Sorti en 2018 par Łukasz Langa. Opinioné : très peu de configuration possible. Il impose un style unique, ce qui évite les débats interminables sur le style en équipe.

**autopep8** — sorti en 2010. Le plus permissif : il corrige uniquement les violations du standard PEP 8 de Python, sans aller plus loin. Laisse plus de liberté mais aussi plus d'incohérences.

> 💡 **PEP 8** : le guide de style officiel de Python, qui définit les conventions de formatage (indentation à 4 espaces, lignes < 79 caractères, etc.). C'est la référence depuis 2001.

### Comparatif

| Critère | Ruff Format | Black | autopep8 |
|---|---|---|---|
| **Vitesse** | ⚡ 10-100x plus rapide que Black | 🐢 Moyen | 🐢 Lent |
| **Opinions** | Très opinioné (style Black) | Très opinioné | ✅ Permissif |
| **Personnalisation** | Limitée (longueur de ligne) | Limitée (longueur de ligne) | Plus flexible |
| **Compatible Black** | ✅ Oui (même style) | — | ❌ Non |
| **Intégration linter** | ✅ Même outil que Ruff linter | ❌ Outil séparé | ❌ Outil séparé |
| **Adoption (2024)** | 🚀 En forte croissance | 🏆 Standard de facto | 📉 En déclin |
| **Un seul outil** | ✅ Lint + Format dans Ruff | ❌ | ❌ |

### Exemples de ce que chaque formateur change

**Avant formatage :**
```python
x={"a":1,"b":2  ,  "c"  :3}
def ma_fonction(   a,b,c   ):
    return a+b+c
```

**Après Black/Ruff Format :**
```python
x = {"a": 1, "b": 2, "c": 3}


def ma_fonction(a, b, c):
    return a + b + c
```

**autopep8** corrigerait seulement les espaces autour des opérateurs, mais pourrait laisser certaines incohérences selon sa configuration.

### Justification du choix

✅ **Choix : Ruff Format**

Si on utilise déjà Ruff comme linter (ce qui est recommandé), utiliser Ruff Format évite d'installer un outil supplémentaire. Il produit exactement le même style que Black, donc compatible avec les projets existants utilisant Black. La vitesse est un bonus sur les gros projets.

Si le projet utilise déjà Black et que l'équipe y est habituée, garder Black reste parfaitement valide — la migration n'est pas obligatoire. Dans tous les cas, éviter autopep8 sur les nouveaux projets : il est trop permissif et son adoption diminue.

---

## 🔒 3. Vérificateurs de types (Type Checkers)

> 💡 **Rappel** : les annotations de types en Python sont **optionnelles**. Tu peux écrire du Python sans jamais en mettre. Mais si tu les ajoutes, un type checker peut détecter des bugs avant l'exécution.

**Exemple concret d'annotation de types :**
```python
# Sans annotation
def additionner(a, b):
    return a + b

# Avec annotations
def additionner(a: int, b: int) -> int:
    return a + b
```

Avec la version annotée, si quelqu'un appelle `additionner("bonjour", 5)`, le type checker détecte l'erreur immédiatement. Sans annotation, Python exécute et plante à l'exécution.

### Les 3 outils

**mypy** — créé en 2012 à Dropbox, c'est **la référence historique**. Il a défini les conventions du typage Python (PEP 484). Écrit en Python. La plupart des tutoriels et documentations parlent de mypy.

**Pyright** — créé par Microsoft, c'est le moteur derrière **Pylance**, l'extension Python de VS Code. Écrit en TypeScript/Node.js. 3 à 5x plus rapide que mypy. Si tu utilises VS Code, tu utilises déjà Pyright sans le savoir.

**Pyre** — créé par Meta (Facebook) pour gérer leur énorme codebase Python. Livré avec **Pysa**, un outil d'analyse de sécurité ("taint analysis"). Plus complexe à configurer.

### Comparatif

| Critère | mypy | Pyright | Pyre |
|---|---|---|---|
| **Vitesse** | 🐢 Lent | ⚡ 3-5x plus rapide | ⚡ Rapide |
| **Précision** | ✅ Haute | ✅ Haute | ✅ Haute |
| **Intégration VS Code** | Via extension | ✅ Natif (Pylance) | Via extension |
| **Inférence sans annotations** | ❌ Limitée (ignore les fonctions non annotées par défaut) | ✅ Forte | ✅ Forte |
| **Documentation** | 🏆 Très complète | ✅ Bonne | 📉 Limitée |
| **Communauté** | 🏆 Très large | 🏆 Très large | Restreinte |
| **Analyse sécurité** | ❌ Non | ❌ Non | ✅ Via Pysa |
| **Facilité de prise en main** | ✅ Simple | ✅ Simple | 🔧 Complexe |
| **Créateur** | Équipe mypy / Dropbox | Microsoft | Meta (Facebook) |

### Comportement différent entre mypy et Pyright

Un point important : **mypy par défaut ignore les fonctions sans annotations**. Si tu écris :

```python
def ma_fonction(x):      # pas d'annotation
    return x + "bonjour"
```

mypy ne signalera rien. Pyright, lui, essaiera d'inférer le type de `x` même sans annotation et pourra détecter des problèmes. Pour que mypy vérifie aussi le code non annoté, il faut ajouter `--check-untyped-defs`.

### Justification du choix

✅ **Choix : mypy** (pour débuter) **+ Pyright** (pour VS Code)

En pratique, ce n'est pas vraiment un choix exclusif : si tu utilises VS Code, tu bénéficies de Pyright automatiquement via Pylance pour le feedback en temps réel dans l'éditeur. Pour la CI/CD, mypy reste la référence avec la documentation la plus complète et la communauté la plus large.

Pyre n'est pertinent que si tu travailles sur une très grosse codebase et que tu as besoin de Pysa pour l'analyse de sécurité.

---

## 🧪 4. Frameworks de tests

> 💡 **Test unitaire** : tester une fonction isolément pour vérifier qu'elle produit le bon résultat. `additionner(2, 3)` doit retourner `5`. **Test d'intégration** : tester que plusieurs parties du code fonctionnent ensemble.

### Les 2 outils

**pytest** — framework tiers (à installer via pip), créé en 2004. Le plus utilisé aujourd'hui : 52%+ des développeurs Python l'utilisent. Simple, lisible, très extensible.

**unittest** — intégré à Python depuis la version 2.1. Inspiré de JUnit (Java). Aucune installation requise. Approche orientée objet avec des classes et méthodes.

### Exemple de code côte à côte

**La même fonction testée des deux façons :**

```python
# La fonction à tester
def additionner(a: int, b: int) -> int:
    return a + b
```

**Avec unittest :**
```python
import unittest

class TestAdditionner(unittest.TestCase):    # doit hériter de TestCase
    def test_addition_normale(self):          # méthode préfixée test_
        self.assertEqual(additionner(2, 3), 5)   # méthode spéciale assertEqual
    
    def test_nombres_negatifs(self):
        self.assertEqual(additionner(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()
```

**Avec pytest :**
```python
def test_addition_normale():           # simple fonction, pas de classe
    assert additionner(2, 3) == 5     # assert Python natif, pas de méthode spéciale

def test_nombres_negatifs():
    assert additionner(-1, 1) == 0
```

> 💡 Le code pytest est bien plus court et plus lisible. Pas de classe, pas de méthodes spéciales. `assert` natif Python = moins à mémoriser.

### Comparatif

| Critère | pytest | unittest |
|---|---|---|
| **Installation** | `pip install pytest` | ✅ Intégré à Python |
| **Syntaxe** | Simple, fonctions Python standard | Verbeux, classes obligatoires |
| **Découverte des tests** | Automatique (cherche `test_*.py`) | ✅ Automatique aussi |
| **Assertions** | `assert` natif + messages d'erreur enrichis | Méthodes spéciales (`assertEqual`, `assertTrue`...) |
| **Fixtures** | ✅ Système puissant et flexible | ❌ setUp/tearDown basique |
| **Paramétrage** | ✅ `@pytest.mark.parametrize` | Limité |
| **Plugins** | ✅ 1000+ (pytest-cov, pytest-mock...) | ❌ Peu extensible |
| **Compatible avec unittest** | ✅ Peut lancer les tests unittest | — |
| **Adoption** | 🏆 52%+ des devs Python | Decreases avec les nouveaux projets |
| **CI/CD** | ✅ Idéal (exit codes propres) | ✅ Fonctionnel |

> 💡 **Fixtures pytest** : système pour préparer des données ou des ressources avant un test et les nettoyer après. Par exemple, créer une connexion à une base de données test avant les tests et la fermer après. Plus flexible que setUp/tearDown d'unittest.

### Justification du choix

✅ **Choix : pytest**

pytest est le choix standard pour les nouveaux projets. Sa syntaxe réduit le code boilerplate (code répétitif sans valeur ajoutée), ses messages d'erreur sont plus clairs pour débugger, et son écosystème de plugins est immense. La compatibilité avec unittest permet de migrer progressivement si nécessaire.

unittest reste pertinent uniquement dans les contextes où l'installation de packages tiers est impossible, ou pour maintenir une codebase legacy qui l'utilise déjà.

---

## 🔐 5. Scanners de sécurité (FACULTATIF)

> 💡 **Rappel** : il existe deux types de vulnérabilités à scanner. (1) Les **vulnérabilités dans ton code** (mots de passe codés en dur, injections SQL...) — c'est le rôle de Bandit. (2) Les **vulnérabilités dans tes dépendances** (une version de requests qui a une faille connue) — c'est le rôle de Safety et Trivy.

### Les 4 outils

**Bandit** — outil d'analyse statique Python open source, maintenu par PyCQA. Analyse l'AST de ton code pour détecter des patterns dangereux : mots de passe en dur, appels `eval()`, usages de `pickle` avec données non fiables, etc.

**Safety** — vérifie tes dépendances Python (`requirements.txt`, `pyproject.toml`) contre une base de données de vulnérabilités connues. Freemium : gratuit pour un usage basique.

**Snyk** — plateforme commerciale complète : analyse le code (SAST), les dépendances (SCA), les images Docker, l'Infrastructure as Code. Très populaire en entreprise. Prix élevé à l'échelle.

**Trivy** — scanner open source d'Aqua Security. Analyse les images Docker, les fichiers de dépendances, les configurations Kubernetes. Ultra-rapide, MIT license (entièrement gratuit).

### Comparatif

| Critère | Bandit | Safety | Snyk | Trivy |
|---|---|---|---|---|
| **Ce qu'il scanne** | Code Python (SAST) | Dépendances Python | Code + Deps + Docker + IaC | Docker + Deps + Config |
| **Prix** | ✅ Gratuit / Open source | Freemium | 💰 Commercial (cher) | ✅ Gratuit / Open source |
| **Vitesse** | ⚡ Rapide | ⚡ Rapide | Moyen | ⚡ Très rapide |
| **Faux positifs** | ~15% (configurable) | Faible | Faible (ML) | Faible |
| **Intégration CI/CD** | ✅ Simple | ✅ Simple | ✅ Très bien intégré | ✅ Simple |
| **Détection Docker** | ❌ Non | ❌ Non | ✅ Oui | ✅ Oui |
| **Interface web** | ❌ Non | ✅ Partielle | ✅ Complète | ❌ CLI seulement |
| **Complexité** | ✅ Simple | ✅ Simple | 🔧 Complexe | ✅ Simple |

### Exemple Bandit en action

```python
# Ce code contient des problèmes de sécurité
import subprocess
password = "monsupermotdepasse123"   # B105: mot de passe codé en dur
subprocess.call(["ls", user_input], shell=True)  # B602: injection de commande
```

```bash
$ bandit mon_code.py
Issue: [B105] Hardcoded password string
Issue: [B602] subprocess call with shell=True identified
```

### Justification du choix

✅ **Choix pour un projet étudiant/startup : Bandit + Trivy**

La combinaison Bandit + Trivy couvre les deux axes essentiels (code + dépendances/Docker) gratuitement et simplement. Bandit s'intègre en une ligne dans GitHub Actions, Trivy aussi.

Safety est une alternative à Trivy pour les dépendances Python uniquement. Snyk est puissant mais son prix est justifié uniquement en entreprise avec des équipes importantes et des projets critiques.

---

## 📋 Tableau récapitulatif global

| Outil | Catégorie | Avantages | Inconvénients | Note /10 | Choix ? |
|---|---|---|---|---|---|
| **Ruff** | Linter | Ultra-rapide (Rust), 800+ règles, auto-fix, remplace Flake8 + isort + plus | Pas de plugins tiers, inférence de types limitée | 9/10 | ✅ |
| **Flake8** | Linter | Mature, extensible, écosystème de plugins énorme | Lent, nécessite de nombreux plugins séparés | 6/10 | ⚠️ Legacy |
| **Pylint** | Linter | Le plus complet, inférence de types, score qualité | Très lent, bruyant sans configuration, en déclin | 7/10 | ⚠️ Cas spécifiques |
| **Ruff Format** | Formateur | Ultra-rapide, même style que Black, même outil que Ruff linter | Peu personnalisable | 9/10 | ✅ |
| **Black** | Formateur | Standard de facto, opinioné (fin des débats de style), grande communauté | Lent sur gros projets, peu personnalisable | 8/10 | ✅ Si déjà installé |
| **autopep8** | Formateur | Permissif, respecte PEP 8 | Trop permissif = incohérences possibles, en déclin | 5/10 | ❌ |
| **mypy** | Type checker | Référence historique, doc excellente, communauté énorme | Lent, ignore les fonctions non annotées par défaut | 8/10 | ✅ |
| **Pyright** | Type checker | 3-5x plus rapide que mypy, natif VS Code (Pylance), forte inférence | Moins de ressources d'apprentissage | 8/10 | ✅ (VS Code) |
| **Pyre** | Type checker | Pysa pour analyse de sécurité, géré par Meta | Complexe à configurer, communauté restreinte | 6/10 | ❌ (sauf gros projets) |
| **pytest** | Tests | Simple, puissant, 1000+ plugins, standard industrie | Installation requise (hors stdlib) | 9/10 | ✅ |
| **unittest** | Tests | Intégré à Python, pas d'installation, familier Java/JUnit | Verbeux, boilerplate important, moins flexible | 6/10 | ⚠️ Legacy |
| **Bandit** | Sécurité (code) | Gratuit, simple, détecte les patterns dangereux Python | Python uniquement, ~15% faux positifs | 8/10 | ✅ |
| **Safety** | Sécurité (deps) | Simple, rapide, spécialisé Python | Freemium, moins complet que Trivy | 7/10 | ⚠️ |
| **Trivy** | Sécurité (Docker/deps) | Gratuit, très rapide, scanne Docker + deps + configs | CLI seulement, pas d'interface web | 9/10 | ✅ |
| **Snyk** | Sécurité (tout) | Complet, interface web, ML pour les faux positifs, remontées PR automatiques | 💰 Très cher à l'échelle, complexe | 8/10 | ⚠️ Entreprise |

---

## 🛠️ Stack recommandée pour un nouveau projet Python

```toml
# pyproject.toml
[dependency-groups]
dev = [
    "ruff>=0.5.0",      # linter + formateur (remplace flake8 + black + isort)
    "mypy>=1.10",       # type checker
    "pytest>=8.0",      # framework de tests
    "pytest-cov>=5.0",  # couverture de code
    "bandit>=1.8",      # scanner de sécurité
]
```

```yaml
# .github/workflows/quality.yml
- name: Lint
  run: uv run ruff check src/

- name: Format check
  run: uv run ruff format --check src/

- name: Type check
  run: uv run mypy src/

- name: Tests
  run: uv run pytest tests/ --cov=src/

- name: Security scan
  run: uv run bandit -r src/
```

> 💡 Cette stack couvre les 4 axes qualité en CI : style, types, tests et sécurité — avec des outils rapides, gratuits et largement adoptés par l'industrie.
