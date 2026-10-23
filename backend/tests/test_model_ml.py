import joblib
import pandas as pd 


def test_model_prediction():

    model = joblib.load(
        "models/prospectia_model.pkl"
    )

    entreprise = pd.DataFrame([
        {
            "effectif":500,
            "chiffre_affaires": 250000000,
            "secteur": "Transport",
            "ville": "Paris",
            "ancien_client": 0, 
            "consommation": 700000,
            "nb_contacts":2
        }
    ])

    prediction = model.predict(entreprise)

    assert len(prediction) ==1 #espero exactamente una predicción porque envié una sola empresa
    assert prediction[0] in [0,1] #la predicción tiene que ser 0 o 1.

