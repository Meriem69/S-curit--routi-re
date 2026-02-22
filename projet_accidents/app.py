from flask import Flask, request, render_template
import joblib
import numpy as np

# Charger le modèle
model = joblib.load("modele_final.pkl")

app = Flask(__name__)


# Page d'accueil
@app.route("/")
def home():
    return render_template("index.html")


# Prédiction
@app.route("/predict", methods=["POST"])
def predict():

    # Récupérer les données du formulaire (14 features)
    lum = float(request.form["lum"])
    agg = float(request.form["agg"])
    inter = float(request.form["int"])
    atm = float(request.form["atm"])
    col = float(request.form["col"])
    catr = float(request.form["catr"])
    catv = float(request.form["catv"])
    heure = float(request.form["heure"])
    jour_semaine = float(request.form["jour_semaine"])
    weekend = float(request.form["weekend"])
    sexe = float(request.form["sexe"])
    age = float(request.form["age"])
    secu1 = float(request.form["secu1"])
    terre_plein = float(request.form["terre_plein"])  # NOUVEAU

    # Créer le tableau (14 features)
    input_data = np.array(
        [
            [
                lum,
                agg,
                inter,
                atm,
                col,
                catr,
                catv,
                heure,
                jour_semaine,
                weekend,
                sexe,
                age,
                secu1,
                terre_plein,
            ]
        ]
    )

    # Prédire
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]

    # Résultat
    if prediction == 1:
        resultat = "⚠️ ACCIDENT GRAVE"
        couleur = "danger"
    else:
        resultat = "✅ ACCIDENT PAS GRAVE"
        couleur = "success"

    return render_template(
        "index.html", prediction=resultat, couleur=couleur, proba=f"{proba * 100:.1f}"
    )


if __name__ == "__main__":
    app.run(debug=True)
