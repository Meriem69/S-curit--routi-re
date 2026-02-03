# 🚗 Prédiction de Gravité des Accidents de la Route

## Description
Application de Machine Learning qui prédit la gravité d'un accident de la route en fonction de ses circonstances (lieu, heure, conditions météo, type de véhicule, etc.).

## Structure du projet
```
projet_accidents/
├── app_fastapi.py          # API FastAPI
├── modele_final.pkl        # Modèle ML sauvegardé
├── features.pkl            # Liste des features
├── requirements.txt        # Dépendances Python
├── templates/
│   └── index.html          # Interface web
├── Prediction-accidents.ipynb  # Notebook d'analyse
└── README.md
```

## Installation

### 1. Cloner le projet
```bash
git clone <url_du_repo>
cd projet_accidents
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'API
```bash
python app_fastapi.py
```

L'application sera accessible sur : http://localhost:8000

## Endpoints API

### GET /health
Vérification du statut de l'API.

**Réponse :**
```json
{
    "status": "ok",
    "model_loaded": true,
    "version": "1.0"
}
```

### POST /predict
Prédiction de gravité d'accident.

**Corps de la requête :**
```json
{
    "lum": 1,
    "agg": 1,
    "int": 1,
    "atm": 1,
    "col": 1,
    "catr": 1,
    "catv": 7,
    "heure": 12,
    "jour_semaine": 0,
    "weekend": 0,
    "sexe": 1,
    "age": 30,
    "secu1": 1,
    "terre_plein": 0
}
```

**Réponse :**
```json
{
    "prediction": 1,
    "label": "GRAVE",
    "probabilite_grave": 54.6
}
```

### Documentation interactive
Accédez à la documentation Swagger : http://localhost:8000/docs

## Features utilisées

| Feature | Description |
|---------|-------------|
| lum | Luminosité (1=Jour, 2=Crépuscule, 3=Nuit sans éclairage, 4=Nuit avec éclairage) |
| agg | Agglomération (1=Hors agglo, 2=En agglo) |
| int | Intersection (1=Hors intersection, 2=En X, 3=En T, 6=Giratoire) |
| atm | Météo (1=Normale, 2=Pluie légère, 3=Pluie forte, 4=Neige) |
| col | Type collision (1=Frontale, 2=Arrière, 3=Côté, 7=Sans collision) |
| catr | Catégorie route (1=Autoroute, 2=Nationale, 3=Départementale, 4=Communale) |
| catv | Type véhicule (1=Vélo, 2=Cyclomoteur, 7=Voiture, 31=Moto, etc.) |
| heure | Heure de l'accident (0-23) |
| jour_semaine | Jour (0=Lundi à 6=Dimanche) |
| weekend | Weekend (0=Non, 1=Oui) |
| sexe | Sexe (1=Homme, 2=Femme) |
| age | Âge de la victime |
| secu1 | Équipement sécurité (0=Aucun, 1=Ceinture, 2=Casque) |
| terre_plein | Présence terre-plein (0=Non, 1=Oui) |

## Modèle

- **Algorithme** : Gradient Boosting Classifier
- **Gestion du déséquilibre** : sample_weight='balanced'
- **Performance** :
  - Recall (Grave) : 77.7%
  - Accuracy : 72.1%
  - F1-Score : 0.49

## Données
Source : [Base BAAC - data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024/)

Années utilisées : 2022, 2023, 2024

## Auteurs
Leila, Caroline, Ina & Meriem

## Technologies
- Python 3.11
- FastAPI
- Scikit-learn
- Pandas / NumPy
- Bootstrap 5