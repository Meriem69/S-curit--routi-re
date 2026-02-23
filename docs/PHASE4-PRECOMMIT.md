# PHASE 4 — Pre-commit Hooks

## Concept clé : pourquoi pre-commit ?

Sans pre-commit, le cycle d'erreur est long :

```
tu codes → git commit → git push → CI (3-5 min) → ❌ erreur
→ tu corriges → re-push → CI (3-5 min) → ✅
Total : 10 minutes perdues à chaque erreur
```

Avec pre-commit, le problème est bloqué immédiatement :

```
tu codes → git commit → 🛡️ pre-commit (5 secondes) → ❌ bloqué + corrigé
→ git add → git commit → ✅ → git push → CI ✅ direct
Total : 30 secondes
```

Pre-commit = le premier filet de sécurité, avant même la CI.

---

## Ce qu'on a fait — étape par étape

---

### Étape 1 — Installation de pre-commit

```bash
uv add --dev pre-commit
```

Résultat : pre-commit 4.5.1 installé dans l'environnement uv.

---

### Étape 2 — Création du fichier .pre-commit-config.yaml

Ce fichier dit à pre-commit quels outils lancer à chaque commit.

**Problème rencontré :** VS Code a sauvegardé le fichier dans
`__pycache__/` au lieu de `projet_accidents/`. On a dû le déplacer :

```bash
move __pycache__\.pre-commit-config.yaml .pre-commit-config.yaml
```

**Contenu du fichier :**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace    # supprime espaces fin de ligne
      - id: end-of-file-fixer      # ajoute ligne vide fin de fichier
      - id: check-yaml             # vérifie fichiers yaml valides
      - id: check-added-large-files # bloque gros fichiers (CSV, pkl...)
      - id: detect-private-key     # bloque mots de passe commités
      - id: check-merge-conflict   # bloque marqueurs de conflit git

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]    # corrige automatiquement le style
      - id: ruff-format  # formate automatiquement le code
```

---

### Étape 3 — Installation des hooks dans Git

```bash
uv run pre-commit install
→ pre-commit installed at .git\hooks\pre-commit
```

Maintenant Git lance automatiquement les vérifications à chaque commit.
Le hook est installé dans `.git/hooks/pre-commit` — c'est un script
que Git appelle avant chaque commit.

---

### Étape 4 — Test sur tous les fichiers

```bash
uv run pre-commit run --all-files
```

**Première exécution — problèmes détectés ET corrigés automatiquement :**

```
trim trailing whitespace......Failed → Fixing app_fastapi.py, templates/...
fix end of files..............Failed → Fixing Dockerfile, requirements.txt...
ruff..........................Failed → Found 6 errors (6 fixed)
ruff-format...................Failed → 3 files reformatted
```

**Deuxième exécution — tout vert :**

```
trim trailing whitespace......Passed
fix end of files..............Passed
check yaml....................Passed
check for added large files...Passed
detect private key............Passed
check for merge conflicts.....Passed
ruff..........................Passed
ruff-format...................Passed
```

C'est le comportement normal : la première fois pre-commit corrige,
la deuxième fois tout est propre.

---

### Étape 5 — Problème lors du commit

**Erreur rencontrée :**
```
[ERROR] Your pre-commit configuration is unstaged.
```

**Cause :** pre-commit modifie le fichier `.pre-commit-config.yaml`
(ajoute une ligne vide) mais le fichier modifié n'est pas re-stagé.
Il faut faire `git add` après chaque modification automatique.

**Solution utilisée :**
```bash
git commit -m "chore: add pre-commit hooks configuration" --no-verify
```

`--no-verify` bypasse pre-commit pour ce commit uniquement.
C'est acceptable ici car on est en train d'installer pre-commit lui-même.

> ⚠️ Ne jamais utiliser `--no-verify` en production pour contourner
> les vérifications de sécurité.

---

### Étape 6 — Problème : pre-commit cherche le fichier à la racine

**Cause :** pre-commit cherche `.pre-commit-config.yaml` à la racine
du repo Git, pas dans `projet_accidents/`. On a dû copier le fichier
aux deux endroits :
- `Projet-securite-routiere/.pre-commit-config.yaml` (racine du repo)
- `Projet-securite-routiere/projet_accidents/.pre-commit-config.yaml`

---

## Résumé Phase 4

| Élément | Statut |
|---------|--------|
| pre-commit installé | ✅ |
| `.pre-commit-config.yaml` créé | ✅ |
| Hooks installés dans Git | ✅ |
| `pre-commit run --all-files` → tout vert | ✅ |
| PR mergée dans develop | ✅ |

## Différence pre-commit vs CI

| | Pre-commit | CI (GitHub Actions) |
|---|---|---|
| Quand ? | Avant le commit (local) | Après le push (GitHub) |
| Durée | 5 secondes | 1-3 minutes |
| Peut être bypassé ? | Oui (`--no-verify`) | Non (protégé par règles) |
| Coût | Gratuit | Minutes CI consommées |
| Rôle | Premier filet local | Filet de sécurité global |

Les deux sont complémentaires — pre-commit évite les allers-retours
inutiles avec la CI.

---

## Réponses aux questions de réflexion

### 1. Différence entre pre-commit et CI ?

**Quand chacun s'exécute ?**
- Pre-commit : sur ta machine, AVANT le commit, en 5 secondes
- CI : sur les serveurs GitHub, APRÈS le push, en 1-3 minutes

**Pourquoi avoir les deux ?**
Parce qu'ils ne protègent pas la même chose :
- Pre-commit protège TON travail local — tu catches les erreurs avant même qu'elles partent
- CI protège le repo partagé — même si quelqu'un bypasse pre-commit, la CI bloque

```
Pre-commit = porte d'entrée de ta maison
CI = vigile à l'entrée de l'immeuble
Les deux sont nécessaires
```

---

### 2. Peut-on contourner le pre-commit ?

Oui, avec :
```bash
git commit --no-verify
```

**Est-ce une bonne idée ?**
Non, sauf cas exceptionnels (comme on l'a fait pour commiter
pre-commit lui-même). En production c'est une très mauvaise pratique
car tu envoies du code non vérifié.

**Comment l'empêcher ?**
On ne peut pas l'empêcher techniquement en local — c'est pour ça
que la CI existe en complément. Si quelqu'un bypasse pre-commit,
la CI bloquera quand même sur GitHub.

---

### 3. Pre-commit ralentit-il le développement ?

**Non, il l'accélère.**

- Pre-commit : 5-10 secondes
- Attendre la CI après chaque push : 3-5 minutes
- Corriger, re-pousser, re-attendre la CI : encore 3-5 minutes

En évitant un seul aller-retour CI, pre-commit te fait gagner
5-10 minutes. Sur une journée de travail avec 10 commits,
c'est 1h de gagnée.
