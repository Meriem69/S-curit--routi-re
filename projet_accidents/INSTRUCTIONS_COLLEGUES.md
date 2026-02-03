# 🚀 INSTRUCTIONS FASTAPI - POUR LES COLLÈGUES

## MÉTHODE 1 : AVEC DOCKER (RECOMMANDÉ) 🐳

### Étape 1 : Installer Docker Desktop
1. Télécharger : https://www.docker.com/products/docker-desktop/
2. Installer
3. Redémarrer le PC
4. Lancer Docker Desktop (attendre qu'il soit prêt)

### Étape 2 : Ouvrir le terminal
- Windows : Clic droit sur le dossier `projet_accidents` → "Ouvrir dans le terminal"
- Ou : Ouvrir PowerShell et taper : `cd C:\chemin\vers\projet_accidents`

### Étape 3 : Lancer l'application
```bash
docker-compose up --build
```

### Étape 4 : Ouvrir le navigateur
```
http://localhost:8000
```

### C'est tout ! ✅

---

## MÉTHODE 2 : SANS DOCKER (si Docker ne marche pas)

### Étape 1 : Ouvrir PowerShell

### Étape 2 : Aller dans le dossier
```bash
cd C:\Users\Utilisateur\Documents\projet_accidents
```
(Remplacer par le chemin de votre dossier)

### Étape 3 : Vérifier qu'on est au bon endroit
```bash
dir
```
Vous devez voir : `app_fastapi.py`, `modele_final.pkl`, `templates`, etc.

### Étape 4 : Installer les dépendances
```bash
pip install fastapi uvicorn python-multipart jinja2 joblib numpy scikit-learn==1.5.0 pandas
```

### Étape 5 : Lancer l'application
```bash
python app_fastapi.py
```

### Étape 6 : Ouvrir le navigateur
```
http://localhost:8000
```

PAS `0.0.0.0:8000` ! Taper `localhost:8000` !

---

## ❌ ERREURS FRÉQUENTES ET SOLUTIONS

### Erreur : "No such file or directory"
**Cause** : Vous n'êtes pas dans le bon dossier
**Solution** : 
```bash
cd C:\chemin\vers\projet_accidents
dir
```
Vérifiez que vous voyez `app_fastapi.py`

### Erreur : "sklearn version"
**Cause** : Mauvaise version de scikit-learn
**Solution** :
```bash
pip uninstall scikit-learn -y
pip install scikit-learn==1.5.0 --only-binary=:all:
```

### Erreur : "Module not found"
**Cause** : Dépendances pas installées
**Solution** :
```bash
pip install fastapi uvicorn python-multipart jinja2 joblib numpy pandas
```

### Erreur : "Address already in use"
**Cause** : Le port 8000 est déjà utilisé
**Solution** : Fermer l'autre terminal ou changer le port

### Le navigateur dit "Ce site est inaccessible"
**Cause** : Mauvaise URL
**Solution** : Taper `http://localhost:8000` (pas `0.0.0.0:8000`)

### Le serveur se lance mais pas de formulaire
**Cause** : Le dossier `templates` manque ou est mal placé
**Solution** : Vérifier que `templates/index.html` existe

---

## 📁 STRUCTURE DU DOSSIER (OBLIGATOIRE)

```
projet_accidents/
├── app_fastapi.py      ← Le code Python
├── modele_final.pkl    ← Le modèle ML
├── features.pkl        ← Les features
└── templates/          ← DOSSIER (pas fichier!)
    └── index.html      ← La page web
```

⚠️ ATTENTION : `templates` est un DOSSIER, pas un fichier !

---

## 🔍 COMMANDES DE VÉRIFICATION

### Vérifier Python
```bash
python --version
```
Doit afficher Python 3.x

### Vérifier le dossier actuel
```bash
cd
```
ou
```bash
pwd
```

### Lister les fichiers
```bash
dir
```
ou
```bash
ls
```

### Vérifier les packages installés
```bash
pip list
```

---

## 📞 SI RIEN NE MARCHE

1. Fermez tout
2. Redémarrez le PC
3. Installez Docker Desktop
4. Lancez Docker Desktop
5. Ouvrez PowerShell dans le dossier du projet
6. Tapez : `docker-compose up --build`
7. Ouvrez : `http://localhost:8000`

---

## ✅ CHECKLIST AVANT DE LANCER

- [ ] Docker Desktop est lancé (icône dans la barre des tâches)
- [ ] Je suis dans le bon dossier (je vois `app_fastapi.py` quand je fais `dir`)
- [ ] J'ai tous les fichiers (app_fastapi.py, modele_final.pkl, templates/index.html)
- [ ] J'utilise `localhost:8000` dans le navigateur (pas `0.0.0.0`)

---

**Si ça ne marche toujours pas, envoyez une capture d'écran de l'erreur !**
