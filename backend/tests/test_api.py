from fastapi.testclient import TestClient
from app.model_api import app
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

client = TestClient(app)

def test_get_secteurs():

    response = client.get("/secteurs")

    assert response.status_code == 200

    resultat = response.json()

    assert "secteurs" in resultat
    assert isinstance(resultat["secteurs"], list)
    assert len(resultat["secteurs"]) > 0


def test_get_villes():

    response = client.get("/villes")

    assert response.status_code == 200

    resultat = response.json()

    assert "villes" in resultat
    assert isinstance(resultat["villes"], list)
    assert len(resultat["villes"]) > 0
    

def test_predict_valid():

    data = {
        "effectif": 500,
        "chiffre_affaires": 250000000,
        "secteur": "Transport",
        "ville": "Paris",
        "ancien_client": 0,
        "consommation": 700000,
        "nb_contacts": 2
    }

    headers = {
        "x-api-token": API_TOKEN
    }

    response = client.post(
        "/predict",
        json=data,
        headers=headers
    )

    assert response.status_code ==200

    resultat = response.json()

    assert "opportunite" in resultat
    assert resultat["opportunite"] in [0, 1]


def test_predict_invalid_token():

    data = {
        "effectif": 500,
        "chiffre_affaires": 250000000,
        "secteur": "Transport",
        "ville": "Paris",
        "ancien_client": 0,
        "consommation": 700000,
        "nb_contacts": 2
    }

    headers = {
        "x-api-token": "mauvais-token"
    }

    response = client.post(
        "/predict",
        json=data,
        headers=headers
    )

    assert response.status_code == 401


def test_predict_missing_field():

    data = {
        "effectif": 500,
        "chiffre_affaires": 250000000,
        "secteur": "Transport",
        "ville": "Paris",
        "ancien_client": 0,
        "consommation": 700000
    }

    headers = {
        "x-api-token": API_TOKEN
    }

    response = client.post(
        "/predict",
        json=data,
        headers=headers
    )

    assert response.status_code == 422


def test_predict_without_token():

    data = {
        "effectif": 500,
        "chiffre_affaires": 250000000,
        "secteur": "Transport",
        "ville": "Paris",
        "ancien_client": 0,
        "consommation": 700000,
        "nb_contacts": 2
        }

    response = client.post(
        "/predict",
        json=data
        )

    assert response.status_code == 422