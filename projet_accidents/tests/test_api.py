from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient


# On mock joblib.load AVANT d'importer app_fastapi
# pour éviter qu'il cherche le vrai fichier .pkl
@pytest.fixture(autouse=True)
def mock_model():
    mock = MagicMock()
    mock.predict.return_value = np.array([1])
    mock.predict_proba.return_value = np.array([[0.3, 0.7]])
    with patch("joblib.load", return_value=mock):
        yield mock


@pytest.fixture
def client(mock_model):
    from app_fastapi import app
    return TestClient(app)


# =====================
# TEST 1 : health check
# =====================
def test_health_check(client):
    """L'endpoint /health doit retourner status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


# =====================
# TEST 2 : prédiction JSON
# =====================
def test_predict_json(client):
    """L'endpoint /predict doit retourner une prédiction"""
    with patch("app_fastapi.save_prediction"):  # mock la BDD
        response = client.post(
            "/predict",
            json={
                "lum": 1,
                "agg": 1,
                "int": 1,
                "atm": 1,
                "col": 1,
                "catr": 2,
                "catv": 7,
                "heure": 14,
                "jour_semaine": 2,
                "weekend": 0,
                "sexe": 1,
                "age": 35,
                "secu1": 1,
                "terre_plein": 0,
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert "probabilite_grave" in data
    assert data["label"] in ["GRAVE", "PAS GRAVE"]


# =====================
# TEST 3 : valeurs de retour
# =====================
def test_predict_returns_grave(client):
    """Quand le modèle prédit 1, le label doit être GRAVE"""
    with patch("app_fastapi.save_prediction"):
        response = client.post(
            "/predict",
            json={
                "lum": 1, "agg": 1, "int": 1, "atm": 1,
                "col": 1, "catr": 2, "catv": 7, "heure": 14,
                "jour_semaine": 2, "weekend": 0, "sexe": 1,
                "age": 35, "secu1": 1, "terre_plein": 0,
            },
        )
    assert response.json()["label"] == "GRAVE"
    assert response.json()["prediction"] == 1


# =====================
# TEST 4 : page d'accueil
# =====================
def test_home_page(client):
    """La page d'accueil doit retourner du HTML"""
    with patch("app_fastapi.init_db"):
        response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]