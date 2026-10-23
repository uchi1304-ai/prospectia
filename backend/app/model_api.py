from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN")

model = joblib.load("models/prospectia_model.pkl")

df_options = pd.read_csv(
    "data/entreprises_clean.csv",
    dtype={"siren": str}
)


class EntrepriseInput(BaseModel):
    effectif: float
    chiffre_affaires: float
    secteur: str
    ville: str
    ancien_client: int
    consommation: float
    nb_contacts: int


@app.get("/secteurs")
def get_secteurs():
    secteurs = sorted(
        df_options["secteur"].dropna().unique().tolist()
    )
    return {"secteurs": secteurs}


@app.get("/villes")
def get_villes():
    villes = sorted(
        df_options["ville"].dropna().unique().tolist()
    )
    return {"villes": villes}


@app.post("/predict")
def predict(
    entreprise: EntrepriseInput,
    x_api_token: str = Header(...)
):

    if x_api_token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )

    df = pd.DataFrame([
        entreprise.model_dump()
    ])

    prediction = model.predict(df)

    return {
        "opportunite": int(prediction[0])
    }