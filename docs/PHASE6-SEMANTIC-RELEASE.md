# PHASE 6 — Semantic Release Automatique

## Contexte : on est toujours dans la CI !

Rappel du pipeline complet qu'on a construit depuis le début :

```
Phase 4 : Pre-commit (local, avant chaque commit)
    ↓
git push → Phase 3 : CI (lint + typecheck + security + tests)
    ↓
Merge dans develop → Phase 5 : Build Docker → GHCR
    ↓
Merge develop → main → Phase 6 : Semantic Release → v0.1.0 🏷️
    ↓
Sync develop avec main automatiquement
```

La Phase 6 est la dernière brique de la CI. Elle ferme la boucle :
après tous les contrôles qualité, elle crée automatiquement une version
officielle de l'application.

---

## Mots clés importants

**SemVer** (Semantic Versioning) : format de versionnage standard MAJOR.MINOR.PATCH

**CHANGELOG** : fichier qui liste tous les changements entre chaque version

**Tag Git** : une étiquette sur un commit qui marque une version officielle (ex: v0.1.0)

**GitHub Release** : une publication officielle sur GitHub avec notes de version,
fichiers téléchargeables, etc.

**workflow_run** : déclencheur GitHub Actions qui attend qu'un autre workflow
soit terminé avant de démarrer

**prerelease** : version de test sur develop (ex: 0.1.0.dev1) avant la release
stable sur main

---

## Concept clé : Semantic Versioning

Format : MAJOR.MINOR.PATCH → exemple : 1.4.2

| Partie | Quand ? | Exemple |
|--------|---------|---------|
| PATCH | Correction de bug | 1.4.2 → 1.4.3 |
| MINOR | Nouvelle fonctionnalité | 1.4.0 → 1.5.0 |
| MAJOR | Changement cassant | 1.0.0 → 2.0.0 |

### Lien direct avec les Conventional Commits

```
fix: correction connexion BDD    → PATCH  (0.1.0 → 0.1.1)
feat: ajout pagination API       → MINOR  (0.1.0 → 0.2.0)
feat!: refonte complète de l'API → MAJOR  (0.1.0 → 1.0.0)
```

C'est pourquoi les Conventional Commits sont absolument critiques
en Phase 6 — semantic-release lit l'historique Git pour décider
quelle version créer.

---

## Ce qu'on a fait — étape par étape

### Étape 1 — Configuration pyproject.toml

On a ajouté la section [project] avec la version initiale
et configuré semantic-release :

```toml
[project]
name = "projet-accidents"
version = "0.1.0"

[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
upload_to_pypi = false
upload_to_release = true
build_command = ""      # pas de build Python nécessaire

[tool.semantic_release.branches.main]
match = "main"
prerelease = false      # releases stables sur main

[tool.semantic_release.branches.develop]
match = "develop"
prerelease = true
prerelease_token = "dev"
```

**Erreurs rencontrées et corrigées :**

1. build_command = false → erreur pydantic car doit être une chaîne
   → corrigé en build_command = ""

2. changelog_file dans la mauvaise section → déprécié dans semantic-release v10
   → supprimé

3. Ligne minor_tags tronquée en "mi" dans le fichier
   → problème de copier-coller, corrigé manuellement dans VS Code

---

### Étape 2 — Workflow release.yml

Le déclencheur clé :
```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types:
      - completed
    branches:
      - main
      - develop
```

workflow_run signifie : attend que la CI soit terminée avant de démarrer.
C'est le principe fondamental — on ne crée jamais une release à partir
de code non testé.

La condition de sécurité :
```yaml
if: ${{ github.event.workflow_run.conclusion == 'success' }}
```
Si la CI a échoué → semantic-release ne tourne pas.

Ce que fait semantic-release automatiquement :
1. Analyse tous les commits depuis la dernière release
2. Détermine le type de bump (MAJOR/MINOR/PATCH)
3. Met à jour version dans pyproject.toml
4. Crée un tag Git (ex: v0.1.0)
5. Génère le CHANGELOG.md
6. Crée une GitHub Release officielle

---

### Étape 3 — Workflow sync-develop.yml

Après chaque release, semantic-release ajoute un commit automatique
("chore: bump version to 0.1.0") sur main. Sans synchronisation,
develop devient en retard sur main.

Ce workflow synchronise develop avec main automatiquement
après chaque push sur main.

---

### Étape 4 — Problèmes de permissions rencontrés

Problème 1 : github-actions[bot] refusé sur develop
```
Permission denied to github-actions[bot]
```
Solution : GitHub → Settings → Actions → General →
Workflow permissions → Read and write permissions → Save

Problème 2 : semantic-release refusé sur main
```
remote: - Changes must be made through a pull request.
```
Cause : la protection de main empêche tout push direct, même du bot.
Solution : désactiver temporairement "Require a pull request"
sur la règle protect-main.

Note : En entreprise on configure plutôt une bypass list spécifique
pour le bot github-actions[bot] plutôt que de désactiver toute protection.

---

### Résultat final

```
✅ Semantic Release tourne en 59 secondes
✅ v0.1.0 créée automatiquement
✅ Tag Git v0.1.0 créé sur GitHub
✅ GitHub Release publiée
✅ develop synchronisé avec main
✅ CHANGELOG.md généré
```

---

## Réponses aux questions de réflexion

### 1. Pourquoi le versionnage automatique ?

**Versionnage manuel :**
- Un développeur décide subjectivement de la version
- Risque d'oubli : on merge 3 features mais on oublie de bumper
- Subjectif : "est-ce un MINOR ou un MAJOR ?"
- CHANGELOG écrit à la main → incomplet, vague, ou pas fait du tout

**Versionnage automatique :**
- La version est déterminée objectivement par les commits
- Impossible d'oublier — c'est dans le pipeline CI
- Cohérence garantie : même règle pour tout le monde
- CHANGELOG exhaustif car basé sur tout l'historique Git

**Erreurs humaines évitées :**
- Oublier de bumper après un merge urgent vendredi soir
- Bumper en MAJOR alors que c'est juste un MINOR
- Créer un tag Git mais oublier la GitHub Release
- CHANGELOG qui mentionne seulement 2 des 8 changements réels

---

### 2. Conventional Commits : critique pour semantic-release ?

OUI, c'est la condition absolue. Semantic-release ne peut rien faire
sans Conventional Commits. C'est sa seule source d'information.

**Avantages :**
- Versionnage 100% automatique et cohérent
- CHANGELOG lisible et structuré automatiquement
- Historique Git compréhensible par n'importe qui
- Intégration possible avec d'autres outils (Jira, Slack)

**Inconvénients :**
- Discipline stricte requise de TOUTE l'équipe, sans exception
- Un seul développeur qui écrit "fixed the bug" au lieu de "fix: bug"
  et ce commit est ignoré par semantic-release
- Courbe d'apprentissage pour les nouveaux membres

**Discipline nécessaire :**
- Configurer commitlint dans pre-commit pour valider le format
- Former les nouveaux développeurs dès le premier jour
- Mettre des exemples dans le README du repo
- Vérifier les messages de commit lors des code reviews

---

### 3. CHANGELOG automatique

**Qui le lit ?**
- Les développeurs de l'équipe : pour comprendre ce qui a changé
- Les développeurs externes : pour savoir si une mise à jour casse leur intégration
- Les tech leads / managers : pour suivre l'avancement réel
- Les équipes QA : pour savoir exactement quoi tester dans chaque release
- Les utilisateurs de l'API : pour anticiper les BREAKING CHANGES

**Utilité concrète :**

Sans CHANGELOG, un développeur qui intègre ton API ne sait pas
ce qui a changé entre v1.2 et v1.3. Il doit lire tout le code.

Avec CHANGELOG automatique :
```markdown
## v1.3.0 (2026-02-23)

### Features
- feat(predict): add confidence score to prediction response
- feat(api): add pagination to history endpoint

### Bug Fixes
- fix(db): handle connection timeout gracefully
```

Il voit immédiatement : "ah, /predict retourne maintenant un champ
confidence_score — je dois mettre à jour mon code."

---

## La vraie question : qui fait quoi en entreprise ?

### Ce que tu as vécu sur ce brief

Tu as tout configuré seule. C'est normal pour un brief individuel.
Mais en entreprise, c'est très différent.

### Réponse directe : NON, pas tout le monde configure tout

Une seule personne (le tech lead ou le DevOps) configure tout
une seule fois. Ensuite les développeurs n'ont qu'à coder.

### Qui configure l'infrastructure CI/CD ?

Le tech lead configure une seule fois :
- La structure des branches (main, develop, feature/)
- Les protections de branches
- Tous les workflows GitHub Actions (ci.yml, build.yml, release.yml)
- Le pre-commit et les règles de qualité
- La configuration semantic-release

Durée : 1 à 2 jours pour tout mettre en place correctement.
Ensuite : ça tourne tout seul, sans intervention.

### Ce que chaque développeur fait au quotidien

```bash
# Une seule fois à l'arrivée dans l'équipe :
git clone https://github.com/entreprise/projet.git
uv run pre-commit install

# Chaque jour :
git checkout -b feature/ma-fonctionnalite
# ... coder ...
git add .
git commit -m "feat: add ma fonctionnalite"
# pre-commit vérifie automatiquement ✅
git push origin feature/ma-fonctionnalite
# ouvrir une PR sur GitHub → c'est tout
```

Le développeur ne touche jamais aux workflows, ne configure rien,
ne crée pas de releases manuellement.

---

## Scénario entreprise complet : 4 développeurs sur le projet accidents

```
Équipe : Leila (tech lead), Caroline, Ina, Meriem

─────────────────────────────────────────────────────
JOUR 1 : Leila configure tout (une seule fois)
─────────────────────────────────────────────────────
✅ Crée le repo + branches main/develop
✅ Configure les protections (PR obligatoire, 1 reviewer)
✅ Crée ci.yml, build.yml, release.yml, sync-develop.yml
✅ Configure pre-commit et pyproject.toml
✅ Documente dans le README comment contribuer

─────────────────────────────────────────────────────
SPRINT 1 (2 semaines) : les 3 devs codent normalement
─────────────────────────────────────────────────────

Caroline fait sa feature :
  git checkout -b feature/add-pagination
  git commit -m "feat(api): add pagination to predict endpoint"
  → PR ouverte → CI verte automatiquement ✅
  → Ina review le code
  → Merge dans develop ✅

Ina corrige un bug :
  git checkout -b fix/db-connection
  git commit -m "fix(db): handle connection timeout"
  → PR → CI verte ✅ → Caroline review → Merge develop ✅

Meriem ajoute une feature :
  git checkout -b feature/confidence-score
  git commit -m "feat(predict): add confidence score to response"
  → PR → CI verte ✅ → Leila review → Merge develop ✅

─────────────────────────────────────────────────────
FIN DE SPRINT : Leila crée la release en 2 clics
─────────────────────────────────────────────────────

PR develop → main
→ CI verte sur main ✅
→ Semantic Release analyse automatiquement :
    feat(api)     → MINOR
    fix(db)       → PATCH
    feat(predict) → MINOR
    Le plus grand = MINOR → version 0.2.0
→ Tag v0.2.0 créé automatiquement
→ CHANGELOG.md mis à jour
→ GitHub Release publiée
→ Image Docker taguée :v0.2.0 sur GHCR
→ develop synchronisé avec main

Tout s'est passé automatiquement après le merge dans main ✅
```

### Ce que chaque membre de l'équipe doit savoir

| Rôle | Configure l'infra | Travail quotidien |
|------|-------------------|-------------------|
| Tech lead | Oui, une seule fois | Code + reviews + merges |
| Développeur | Non | Conventional commits + PRs + reviews |
| Tous | - | Ne jamais pusher directement sur main |

### La règle d'or

Une fois l'infra configurée, les développeurs n'ont qu'une
seule responsabilité : écrire de bons Conventional Commits.
Le reste est entièrement automatique.

---

## Bilan complet du brief CI/CD

| Phase | Description | Statut |
|-------|-------------|--------|
| Phase 0 | Veille technique CI/CD | ✅ |
| Phase 1 | Analyse qualité avec ruff (658 erreurs, 25 problèmes) | ✅ |
| Phase 2 | GitFlow + Conventional Commits + protection branches | ✅ |
| Phase 3 | Pipeline CI (lint, typecheck, security, tests) | ✅ |
| Phase 4 | Pre-commit hooks | ✅ |
| Phase 5 | Docker + publication sur GHCR | ✅ |
| Phase 6 | Semantic Release + v0.1.0 créée automatiquement | ✅ |
| Phase 7 | Bonus — déploiement Azure Container Apps | ⏭️ |
| Phase 8 | Bonus — monitoring | ⏭️ |

Ce qui tourne automatiquement désormais sur le projet :
- Chaque commit → pre-commit vérifie le code en 5 secondes
- Chaque PR → CI complète (lint + tests + security) en 30 secondes
- Chaque merge dans develop → image Docker buildée et publiée sur GHCR
- Chaque merge dans main → nouvelle version créée automatiquement
