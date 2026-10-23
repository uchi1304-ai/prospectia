import joblib
import pandas as pd


model = joblib.load("models/prospectia_model.pkl")

entreprise = pd.DataFrame([
    {
        "effectif":500,
        "chiffre_affaires": 250000000, 
        "secteur": "Transport",
        "ville": "Paris",
        "ancien_client": 0,
        "consommation": 700000,
        "nb_contacts": 2
    }
])

prediction = model.predict(entreprise)

print(prediction)
