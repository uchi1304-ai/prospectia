import streamlit as st
import requests
import os

from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

API_BASE_URL = "http://backend:8000"
API_URL = f"{API_BASE_URL}/predict"


response_secteurs = requests.get(
    f"{API_BASE_URL}/secteurs"
)

response_villes = requests.get(
    f"{API_BASE_URL}/villes"
)

secteurs = response_secteurs.json()["secteurs"]
villes = response_villes.json()["villes"]


st.title("ProspectIA")
st.write("Prédiction d'opportunité commerciale")


effectif = st.number_input(
    "Effectif",
    min_value=0,
    value=500
)

chiffre_affaires = st.number_input(
    "Chiffre d'affaires",
    min_value=0.0,
    value=250000000.0
)

secteur = st.selectbox(
    "Secteur",
    options=secteurs
)

ville = st.selectbox(
    "Ville",
    options=villes
)

ancien_client_label = st.selectbox(
    "Ancien client",
    options=["Non", "Oui"]
)

ancien_client = (
    1 if ancien_client_label == "Oui"
    else 0
)

consommation = st.number_input(
    "Consommation",
    min_value=0.0,
    value=700000.0
)

nb_contacts = st.number_input(
    "Nombre de contacts",
    min_value=0,
    value=2
)


if st.button("Prédire"):

    data = {
        "effectif": effectif,
        "chiffre_affaires": chiffre_affaires,
        "secteur": secteur,
        "ville": ville,
        "ancien_client": ancien_client,
        "consommation": consommation,
        "nb_contacts": nb_contacts
    }

    headers = {
        "x-api-token": API_TOKEN
    }

    response = requests.post(
        API_URL,
        json=data,
        headers=headers
    )

    if response.status_code == 200:

        resultat = response.json()

        opportunite = resultat["opportunite"]

        if opportunite == 1:
            st.success(
                "Opportunité commerciale détectée"
            )
        else:
            st.warning(
                "Pas d'opportunité commerciale détectée"
            )

    else:
        st.error(
            f"Erreur API : {response.status_code}"
        )