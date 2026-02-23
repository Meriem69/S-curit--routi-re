# PHASE 2 — Stratégie de Branches & Conventional Commits

## Concepts clés

### Pourquoi GitFlow ?

Sans organisation, plusieurs développeurs qui travaillent en même temps sur le même
code créent du chaos : le code d'une personne écrase celui d'une autre, rien n'est
vérifié avant d'aller en production.

GitFlow résout ça avec 3 niveaux de branches :

```
main          → la production. Seulement ce qui est parfait et testé.
  ↑ PR uniquement quand c'est prêt
develop       → la cuisine. Tout le monde intègre son travail ici.
  ↑ PR depuis chaque feature
feature/xxx   → ton plan de travail isolé. Tu travailles ici sans déranger les autres.
```

**Règle absolue : on ne travaille jamais directement sur `main` ou `develop`.**

---

### Pourquoi protéger les branches ?

Sans protection, n'importe qui peut faire `git push origin main` et casser la
production en sautant tous les filets de sécurité. La protection force à passer
par le chemin correct : feature → PR → CI → approbation → merge.

---

### Pourquoi les Conventional Commits ?

Au lieu de commits comme "modif", "fix truc", "ça marche"... on suit un format
strict que des outils peuvent lire automatiquement pour générer les numéros de
version et les changelogs.

Format obligatoire :
```
<type>(<scope>): <description>
```

Types disponibles :

| Type | Description | Impact version |
|------|-------------|----------------|
| feat | Nouvelle fonctionnalité | MINOR 0.1.0 → 0.2.0 |
| fix | Correction de bug | PATCH 0.1.0 → 0.1.1 |
| style | Formatage, espaces | Aucun |
| refactor | Refactorisation | Aucun |
| docs | Documentation | Aucun |
| chore | Maintenance | Aucun |
| ci | CI/CD | Aucun |
| feat! | Breaking change | MAJOR 1.0.0 → 2.0.0 |

---

### Qu'est-ce qu'une Pull Request ?

Une PR = une demande de fusion. Tu dis à l'équipe :
"J'ai travaillé sur cette branche, quelqu'un peut vérifier avant qu'on intègre ?"

Deux niveaux de vérification :
1. **La machine** (automatique) → CI : ruff, tests, sécurité...
2. **Un humain** → le formateur lit le code et approuve ou refuse

Si la CI est rouge → impossible de merger même si un humain veut le faire.

---

## Ce qu'on a fait — étape par étape

---

### Étape 1 — Vérification de l'état du repo

```bash
git status
```

Résultat :
```
On branch main
Changes not staged for commit:
    deleted: INSTRUCTIONS_COLLEGUES.md
Untracked files:
    .python-version
    README.md
    main.py
    pyproject.toml
    uv.lock
```

On a découvert que les fichiers créés en Phase 1 (uv) n'étaient pas encore
commités. `INSTRUCTIONS_COLLEGUES.md` avait été supprimé — pas besoin de le garder.

---

### Étape 2 — Commit des fichiers Phase 1

On ajoute uniquement les fichiers uv (pas `main.py` qui est vide, ni `README.md`
qu'on traitera plus tard) :

```bash
git add pyproject.toml uv.lock .python-version
```

**Pourquoi ces 3 fichiers ?**
- `pyproject.toml` : configuration du projet et ses dépendances (remplace requirements.txt)
- `uv.lock` : verrou des versions exactes — garantit que tout le monde a les mêmes versions
- `.python-version` : indique la version Python à utiliser

Commit avec le format Conventional Commits :
```bash
git commit -m "chore: add uv configuration files (pyproject.toml, uv.lock)"
```

> ⚠️ Les Conventional Commits doivent être en anglais — les outils qui lisent
> ces commits pour générer les versions s'attendent à l'anglais.

---

### Étape 3 — Push sur GitHub

```bash
git push origin main
```

Résultat :
```
To https://github.com/Meriem69/S-curit--routi-re.git
   03ea53c..740c006  main -> main
```

Les fichiers sont maintenant visibles sur GitHub.

---

### Étape 4 — Création de la branche develop

```bash
git checkout -b develop
git push -u origin develop
```

**Ce qui se passe :**
- `git checkout -b develop` : crée la branche `develop` localement et bascule dessus
- `git push -u origin develop` : envoie cette branche sur GitHub
- `-u` : lie la branche locale à la branche distante (les prochains push/pull seront automatiques)

Résultat sur GitHub : la branche `develop` apparaît à côté de `main`.

---

### Étape 5 — Création de la feature branch

```bash
git checkout develop
git checkout -b feature/fix-formatting
```

On part toujours de `develop` pour créer une feature branch, jamais de `main`.

**Convention de nommage :** `feature/nom-de-la-feature` avec des tirets.

---

### Étape 6 — Corrections automatiques avec ruff

```bash
uv run ruff check . --fix
```

Résultat :
```
Found 6 errors (6 fixed, 0 remaining).
```

Ruff a corrigé automatiquement : imports inutilisés, f-strings sans variable.

```bash
uv run ruff format .
```

Résultat :
```
3 files reformatted, 1 file left unchanged.
```

Ruff a reformatté : guillemets simples → doubles, espaces en fin de ligne supprimés.

---

### Étape 7 — Vérification des changements

```bash
git diff --stat
```

Résultat :
```
projet_accidents/Prediction-accidents.ipynb | 683 ++++--
projet_accidents/app.py                     |  83 ++--
projet_accidents/app_fastapi.py             | 158 ++---
4 files changed, 554 insertions(+), 543 deletions(-)
```

3 fichiers modifiés par ruff.

---

### Étape 8 — Commit conventionnel

```bash
git add .
git commit -m "style: fix formatting issues detected by ruff (quotes, whitespace, unused imports)"
```

On utilise le type `style` car on ne change pas le comportement du code,
seulement le formatage.

> ⚠️ Erreur faite : le commit a été tapé `stule` au lieu de `style` et
> `formating` au lieu de `formatting`. À éviter en production.

---

### Étape 9 — Push de la feature branch

```bash
git push -u origin feature/fix-formatting
```

Résultat :
```
* [new branch] feature/fix-formatting -> feature/fix-formatting
```

La branche est maintenant visible sur GitHub. GitHub propose automatiquement
de créer une Pull Request depuis cette branche.

---

### Étape 10 — Protection de la branche main

Sur GitHub → Settings → Rules → Rulesets → New branch ruleset

Configuration appliquée :

| Paramètre | Valeur |
|-----------|--------|
| Ruleset Name | protect-main |
| Enforcement status | Active |
| Target branch | main |
| Require a pull request before merging | ✅ |
| Required approvals | 1 |
| Block force pushes | ✅ |

**Effet :** impossible de pousser directement sur `main`. Obligé de passer
par une PR avec au moins 1 approbation.

> Note : "Require status checks to pass" sera ajouté en Phase 3 quand les
> GitHub Actions seront configurées.

---

### Étape 11 — Protection de la branche develop

Même procédure, moins stricte (pas besoin d'approbation humaine) :

| Paramètre | Valeur |
|-----------|--------|
| Ruleset Name | protect-develop |
| Enforcement status | Active |
| Target branch | develop |
| Require a pull request before merging | ✅ |
| Required approvals | 0 |
| Block force pushes | ✅ |

**Effet :** impossible de pousser directement sur `develop` non plus,
mais pas besoin qu'un humain approuve — la CI suffira.

---

### Étape 12 — Création de la Pull Request

Sur GitHub → Pull requests → New pull request

Configuration :
- **base** : `develop`
- **compare** : `feature/fix-formatting`
- **Titre** : `style: fix formatting issues detected by ruff`
- **Description** : détail des corrections effectuées

Résultat : PR #1 ouverte, visible dans l'onglet "Pull requests" du repo.

---

## Résumé Phase 2

| Élément | Statut |
|---------|--------|
| Branche `develop` créée | ✅ |
| Branche `feature/fix-formatting` créée | ✅ |
| Conventional commit effectué | ✅ (avec faute de frappe à corriger) |
| Protection `main` configurée | ✅ |
| Protection `develop` configurée | ✅ |
| Pull Request #1 ouverte | ✅ |

## Ce qui manque encore (sera fait en Phase 3)

- Ajouter les status checks dans les règles de protection (CI doit passer)
- Configurer les GitHub Actions pour que la CI tourne automatiquement sur chaque PR
- Ajouter le formateur comme approbateur sur le repo

---

## Réponses aux questions de réflexion

### 1. Pourquoi protéger les branches ?

**Que se passerait-il sans protection ?**
N'importe qui dans l'équipe pourrait faire `git push origin main` directement
et envoyer du code cassé en production sans aucune vérification.

Exemple concret : une développeuse travaille sur une nouvelle feature,
elle a oublié de tester. Elle push directement sur main. Le site tombe.
Tous les utilisateurs voient une erreur 500.

Avec la protection :
- Impossible de push directement sur main ou develop
- Obligé de passer par une PR
- La CI vérifie automatiquement (tests, lint, sécurité)
- Un humain relit le code avant de merger

---

### 2. Pourquoi des commits conventionnels ?

**Avantages pour l'équipe :**
- L'historique Git devient lisible : on comprend ce qui a changé sans lire le code
- On sait immédiatement si un commit corrige un bug (fix) ou ajoute une feature (feat)
- Facilite les code reviews — le relecteur comprend l'intention du commit

```
# Avant conventional commits
"modif"
"fix truc"
"ça marche enfin"

# Après conventional commits
"feat(predict): add probability score to prediction response"
"fix(db): handle connection timeout in save_prediction"
"style: format files with ruff"
```

**Avantages pour le versionnage automatique :**
Des outils comme semantic-release lisent les commits et génèrent
automatiquement les numéros de version :
- fix: → 1.0.0 → 1.0.1 (PATCH)
- feat: → 1.0.0 → 1.1.0 (MINOR)
- feat!: → 1.0.0 → 2.0.0 (MAJOR)

Plus besoin de décider manuellement "est-ce qu'on passe à la version 2 ?".
C'est déterminé par les commits eux-mêmes.

---

### 3. Différence entre develop et main ?

**develop** = l'environnement de staging, la cuisine
- Toutes les features en cours d'intégration atterrissent ici
- Peut contenir des bugs non critiques
- Les développeurs mergent ici plusieurs fois par semaine

**main** = la production, ce que les utilisateurs voient
- Seulement du code testé, validé, approuvé
- Ne reçoit des merges que lors de releases planifiées

**Quand merger dans develop ?**
- Quand une feature est terminée et les tests passent
- Après review de la PR
- Plusieurs fois par semaine

**Quand merger dans main ?**
- Quand develop est stable et prête pour une release
- Après validation complète (tests + review + approbation)
- Seulement pour les vraies mises en production
