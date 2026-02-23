# PROBLEMES_DETECTES.md — Projet Sécurité Routière

## Comment ces problèmes ont été détectés

### Étape 1 — Vérification que uv est installé

```
uv --version
→ uv 0.9.7 (0adb44480 2025-10-30)
```

### Étape 2 — Initialisation de uv dans le projet

```
uv init --no-package
→ Initialized project `projet-accidents`
```

uv ne trouvait pas de fichier `pyproject.toml` car le projet utilisait l'ancien système
(`requirements.txt`). La commande `uv init` a créé ce fichier nécessaire pour utiliser uv.

### Étape 3 — Installation de ruff

```
uv add --dev ruff
→ + ruff==0.15.2
```

Ruff est installé comme outil de développement (pas en production).
Il combine linter + formateur en un seul outil, écrit en Rust donc très rapide.

### Étape 4 — Analyse basique

```
uv run ruff check .
→ Found 6 errors.
```

Avec les règles de base, ruff a trouvé 6 erreurs : 1 import inutilisé dans
`app_fastapi.py` et 5 problèmes dans le notebook.

### Étape 5 — Analyse complète avec toutes les règles

```
uv run ruff check . --select=ALL --ignore=D,ANN,COM
→ Found 658 errors.
```

En activant toutes les règles disponibles, 658 erreurs détectées sur l'ensemble
du projet (notebook + fichiers Python).

### Étape 6 — Résumé statistique

```
uv run ruff check . --select=ALL --ignore=D,ANN,COM --statistics
```

Résultat obtenu :

| Nb  | Code    | Nom                                  | Auto-corrigeable |
|-----|---------|--------------------------------------|------------------|
| 385 | Q000    | bad-quotes-inline-string             | ✅ oui           |
| 106 | T201    | print                                | ❌ non           |
|  44 | W291    | trailing-whitespace                  | ✅ oui           |
|  25 | E501    | line-too-long                        | ❌ non           |
|  24 | W293    | blank-line-with-whitespace           | ✅ oui           |
|  16 | PD003   | pandas-use-of-dot-is-null            | ❌ non           |
|  14 | FAST002 | fast-api-non-annotated-dependency    | ❌ non           |
|  11 | A003    | builtin-attribute-shadowing          | ❌ non           |
|   7 | PLR2004 | magic-value-comparison               | ❌ non           |
|   4 | BLE001  | blind-except                         | ❌ non           |
|   4 | F541    | f-string-missing-placeholders        | ✅ oui           |
|   4 | I001    | unsorted-imports                     | ✅ oui           |
|   2 | F401    | unused-import                        | ✅ oui           |
|   2 | PLR0913 | too-many-arguments                   | ❌ non           |
|   2 | TRY300  | try-consider-else                    | ❌ non           |
|   2 | W292    | missing-newline-at-end-of-file       | ✅ oui           |
|   1 | A002    | builtin-argument-shadowing           | ❌ non           |
|   1 | PD010   | pandas-use-of-dot-pivot-or-unstack   | ❌ non           |
|   1 | PERF401 | manual-list-comprehension            | ❌ non           |
|   1 | RET504  | unnecessary-assign                   | ❌ non           |
|   1 | S104    | hardcoded-bind-all-interfaces        | ❌ non           |
|   1 | S201    | flask-debug-true                     | ❌ non           |

**Total : 658 erreurs — 463 corrigeables automatiquement avec `ruff --fix`**

---

## Analyse des problèmes par catégorie

---

### 🎨 FORMATAGE (482 erreurs)

#### P01 — Guillemets simples au lieu de doubles (385 occurrences)
**Code ruff :** `Q000 bad-quotes-inline-string`
**Fichiers :** `app.py`, `app_fastapi.py`, `Prediction-accidents.ipynb`
**Exemple détecté :**
```python
model = joblib.load('modele_final.pkl')   # ❌
model = joblib.load("modele_final.pkl")   # ✅
```
**Auto-corrigeable :** oui — `uv run ruff format .`

---

#### P02 — Espaces invisibles en fin de ligne (44 occurrences)
**Code ruff :** `W291 trailing-whitespace`
**Explication :** Des espaces traînent après le code. Invisible à l'œil mais
pollue les diffs Git — chaque commit montre des "modifications" qui n'en sont pas.
**Auto-corrigeable :** oui

---

#### P03 — Lignes blanches contenant des espaces (24 occurrences)
**Code ruff :** `W293 blank-line-with-whitespace`
**Explication :** Des lignes qui semblent vides contiennent en réalité des espaces.
Même problème que P02.
**Auto-corrigeable :** oui

---

#### P04 — Lignes trop longues (25 occurrences)
**Code ruff :** `E501 line-too-long`
**Exemple détecté (`app.py` ligne 36) :**
```python
input_data = np.array([[lum, agg, inter, atm, col, catr, catv, heure, jour_semaine, weekend, sexe, age, secu1, terre_plein]])
# 129 caractères → limite standard = 88
```
**Auto-corrigeable :** non

---

#### P05 — Pas de retour à la ligne en fin de fichier (2 fichiers)
**Code ruff :** `W292 missing-newline-at-end-of-file`
**Fichiers :** `app.py`, `app_fastapi.py`
**Auto-corrigeable :** oui

---

#### P06 — Imports non triés (4 occurrences)
**Code ruff :** `I001 unsorted-imports`
**Exemple (`app_fastapi.py`) :**
```python
# ❌ imports tiers avant bibliothèque standard, psycopg2 importé au milieu du fichier
from fastapi import FastAPI
import os
import psycopg2   # devrait être en haut avec les autres imports
```
**Auto-corrigeable :** oui

---

### 📦 IMPORTS ET CODE MORT (6 erreurs)

#### P07 — Import inutilisé : `datetime` (2 occurrences)
**Code ruff :** `F401 unused-import`
**Fichier :** `app_fastapi.py` ligne 9
```python
from datetime import datetime   # jamais utilisé dans le code
```
**Auto-corrigeable :** oui

---

#### P08 — f-strings sans variable (4 occurrences)
**Code ruff :** `F541 f-string-missing-placeholders`
**Fichier :** `Prediction-accidents.ipynb` cellule 191
```python
print(f"Recall (Grave) : 0.777 (77.7%)")   # ❌ f inutile, pas de {variable}
print("Recall (Grave) : 0.777 (77.7%)")    # ✅
```
**Auto-corrigeable :** oui

---

### 🖨️ PRINT EN PRODUCTION (106 erreurs)

#### P09 — `print()` utilisé à la place de `logging` (106 occurrences)
**Code ruff :** `T201 print`
**Fichiers :** `app_fastapi.py` (6 occurrences), `Prediction-accidents.ipynb` (100 occurrences)
**Explication :** Dans le notebook c'est normal. Dans `app_fastapi.py` c'est
une mauvaise pratique : en production il faut `logging` qui permet de contrôler
le niveau (DEBUG/INFO/ERROR) et la destination des logs.
```python
print(f"Erreur connexion BDD: {e}")          # ❌ production
logging.error(f"Erreur connexion BDD: {e}")  # ✅ production
```
**Auto-corrigeable :** non

---

### 🐼 PANDAS (17 erreurs)

#### P10 — `.isnull()` au lieu de `.isna()` (16 occurrences)
**Code ruff :** `PD003 pandas-use-of-dot-is-null`
**Fichier :** `Prediction-accidents.ipynb`
```python
df.isnull().sum()   # ❌ ancienne méthode
df.isna().sum()     # ✅ méthode préférée (résultat identique)
```

---

#### P11 — `.unstack()` au lieu de `.pivot_table()` (1 occurrence)
**Code ruff :** `PD010 pandas-use-of-dot-pivot-or-unstack`
**Fichier :** `Prediction-accidents.ipynb` cellule 153
```python
df.groupby(['jour_semaine', 'heure']).size().unstack()  # ❌
# ✅ préférer pivot_table() plus lisible et fonctionnel
```

---

### 🏷️ TYPES ET NOMMAGE (19 erreurs)

#### P12 — Attribut de classe qui écrase un builtin Python (11 occurrences)
**Code ruff :** `A003 builtin-attribute-shadowing`
**Fichier :** `app_fastapi.py` ligne 149
```python
class AccidentData(BaseModel):
    int: int   # ❌ "int" est un type Python natif !
```
**Correction :** renommer en `intersection` ou `type_carrefour`

---

#### P13 — Argument de fonction qui écrase un builtin (1 occurrence)
**Code ruff :** `A002 builtin-argument-shadowing`
**Fichier :** `app_fastapi.py`
```python
async def predict_form(int: int = Form(...)):   # ❌ même problème
```

---

#### P14 — Valeurs magiques dans les comparaisons (7 occurrences)
**Code ruff :** `PLR2004 magic-value-comparison`
**Fichier :** `Prediction-accidents.ipynb`
```python
if caract_all['lat'] >= 41 and caract_all['lat'] <= 51:  # ❌ que signifient 41 et 51 ?

LAT_MIN_FRANCE = 41   # ✅ nommer les constantes
LAT_MAX_FRANCE = 51
```

---

### ⚡ FASTAPI (14 erreurs)

#### P15 — Dépendances FastAPI sans `Annotated` (14 occurrences)
**Code ruff :** `FAST002 fast-api-non-annotated-dependency`
**Fichier :** `app_fastapi.py`
```python
async def predict_form(lum: int = Form(...))           # ❌ ancienne syntaxe dépréciée
async def predict_form(lum: Annotated[int, Form()])    # ✅ syntaxe moderne
```

---

### ♻️ ARCHITECTURE ET CODE (10 erreurs)

#### P16 — Trop d'arguments dans une fonction (2 occurrences)
**Code ruff :** `PLR0913 too-many-arguments`
**Fichier :** `app_fastapi.py`
```python
def save_prediction(age, sexe, vehicule, meteo, luminosite, type_route, resultat, probabilite):
# 8 arguments → limite recommandée = 5
# Solution : regrouper dans un objet PredictionData
```

---

#### P17 — `except Exception` trop large (4 occurrences)
**Code ruff :** `BLE001 blind-except`
**Fichier :** `app_fastapi.py`
```python
except Exception as e:                      # ❌ capture TOUT
except psycopg2.OperationalError as e:      # ✅ capture seulement les erreurs BDD
```

---

#### P18 — `return` dans le bloc `try` au lieu de `else` (2 occurrences)
**Code ruff :** `TRY300 try-consider-else`
**Fichier :** `app_fastapi.py`
```python
try:
    conn = psycopg2.connect(...)
    return conn      # ❌ dans le try
except Exception:
    return None

try:                 # ✅ dans le else
    conn = psycopg2.connect(...)
except Exception:
    return None
else:
    return conn
```

---

#### P19 — Variable inutile avant return (1 occurrence)
**Code ruff :** `RET504 unnecessary-assign`
**Fichier :** `app_fastapi.py`
```python
conn = psycopg2.connect(...)
return conn                      # ❌ assignation inutile
return psycopg2.connect(...)     # ✅ retour direct
```

---

#### P20 — Boucle for au lieu de list comprehension (1 occurrence)
**Code ruff :** `PERF401 manual-list-comprehension`
**Fichier :** `Prediction-accidents.ipynb`
```python
# ❌
colonnes_existantes = []
for c in colonnes_a_supprimer:
    if c in df.columns:
        colonnes_existantes.append(c)

# ✅ plus Pythonique et plus rapide
colonnes_existantes = [c for c in colonnes_a_supprimer if c in df.columns]
```

---

### 🔒 SÉCURITÉ (détectés par ruff + inspection manuelle)

#### P21 — `debug=True` dans l'app Flask
**Code ruff :** `S201 flask-debug-true`
**Fichier :** `app.py` ligne 56
```python
app.run(debug=True)   # ❌ DANGER en production
```
En cas d'erreur, active un débogueur interactif accessible depuis le navigateur.
N'importe qui peut exécuter du code Python sur le serveur.

---

#### P22 — Binding sur toutes les interfaces réseau
**Code ruff :** `S104 hardcoded-bind-all-interfaces`
**Fichier :** `app_fastapi.py` ligne 258
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # expose sur toutes les interfaces
```

---

#### P23 — Fichier `.env` commité avec mot de passe (détection manuelle)
**Fichier :** `.env`
```
DB_PASSWORD=password123   # visible par tous sur GitHub
```
Non détectable par ruff — problème de repo Git.

---

#### P24 — Utilisateur root dans le conteneur Docker (détection manuelle)
**Fichier :** `Dockerfile`
Pas d'instruction `USER` → le conteneur tourne en root par défaut.

---

### 📁 STRUCTURE DU REPO (détection manuelle)

#### P25 — README mal nommé
**Fichier :** `README.rd` → doit être `README.md`
GitHub ne reconnaît pas l'extension `.rd`, la page du repo s'affiche sans documentation.

---

## Résumé final

| Catégorie | Problèmes | Erreurs ruff |
|---|---|---|
| 🎨 Formatage | P01 à P06 | 482 |
| 📦 Imports / code mort | P07, P08 | 6 |
| 🖨️ Print en production | P09 | 106 |
| 🐼 Pandas | P10, P11 | 17 |
| 🏷️ Types et nommage | P12 à P14 | 19 |
| ⚡ FastAPI | P15 | 14 |
| ♻️ Architecture | P16 à P20 | 10 |
| 🔒 Sécurité | P21 à P24 | 2 ruff + 2 manuels |
| 📁 Repo | P25 | manuel |
| **Total** | **25 problèmes** | **658 erreurs** |

> 463 erreurs sont corrigeables automatiquement avec : `uv run ruff check . --fix`

---

## Réponses aux questions de réflexion

### 1. Pourquoi protéger les branches ?

**Que se passerait-il sans protection ?**
N'importe qui pourrait pusher directement sur main et casser la production.
Voir réponse complète dans PHASE2-BRANCHES-COMMITS.md.

---

### 2. Pourquoi des commits conventionnels ?

Voir réponse complète dans PHASE2-BRANCHES-COMMITS.md.

---

### 3. Différence entre develop et main ?

Voir réponse complète dans PHASE2-BRANCHES-COMMITS.md.

---

## Réponses aux questions spécifiques Phase 1

### 1. Pourquoi utiliser ruff plutôt que flake8 + black séparément ?

Ruff combine linter (flake8) + formateur (black) en un seul outil écrit en Rust.
Il est 10 à 100x plus rapide que les outils Python équivalents.
Un seul outil à installer, un seul à configurer dans la CI.

### 2. Que signifient les 658 erreurs ?

Ce n'est pas que le code "ne marche pas" — l'application fonctionnait.
Les 658 erreurs représentent des problèmes de qualité :
- 482 erreurs de formatage (guillemets, espaces) → cosmétiques
- 106 print() en production → mauvaise pratique
- 14 dépendances FastAPI non annotées → obsolète
- 2 problèmes de sécurité détectés par ruff + 2 manuels → dangereux

### 3. Pourquoi 463 erreurs sont auto-corrigeables mais pas les 195 autres ?

Les erreurs auto-corrigeables sont purement stylistiques — ruff sait
exactement comment les corriger sans changer le comportement du code.

Les 195 non auto-corrigeables nécessitent une décision humaine :
- Renommer `int` en `intersection` (P12) — ruff ne sait pas quel nom choisir
- Remplacer `print()` par `logging` (P09) — ruff ne sait pas quel niveau de log utiliser
- Corriger `debug=True` (P21) — ruff ne sait pas comment configurer la production
