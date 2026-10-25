from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
import logging
import time 
from fastapi import Request


load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prospectia.monitoring")
metrics = {
    "total_requests":0,
    "total_errors":0,
    "total_predictions":0,
    "total_latency_ms": 0.0
}

@app.middleware("http")
async def monitor_request(request: Request, call_next):
    start = time.perf_counter()
    status_code = 500

    try: 
        response= await call_next(request)
        status_code = response.status_code
        return response

    except Exception: 
        logger.exception(
            "Error interno: method=%s path=%s",
            request.method,
            request.url.path
        )
        raise
    finally: 
        duration_ms = (time.perf_counter() - start) * 1000
        metrics["total_requests"] += 1
        metrics["total_latency_ms"] += duration_ms

        if status_code >= 400:
            metrics["total_errors"] += 1

        if request.url.path == "/predict" and status_code == 200:
            metrics["total_predictions"] += 1


        logger.info(
            "method=%s path=%s status = %s latency_ms=%.2f",
            request.method,
            request.url.path,
            status_code,
            duration_ms
    )


@app.get("/metrics")
def get_metrics(x_api_token: str = Header(...)):
    if not API_TOKEN or x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token invalide")

    total = metrics["total_requests"]

    avg_latency = (
        metrics["total_latency_ms"] / total
        if total > 0 else 0
    )

    return {
        "total_requests": total,
        "total_errors": metrics["total_errors"],
        "total_predictions": metrics["total_predictions"],
        "average_latency_ms": round(avg_latency, 2)
    }
   

API_TOKEN = os.getenv("API_TOKEN")

model = joblib.load("models/prospectia_model.pkl")

@app.get("/health")
def health(): 
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


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


