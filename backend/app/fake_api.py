from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

df = pd.read_csv(
    "data/entreprises_api.csv", 
    dtype= {"siren":str}
    )

@app.get("/entreprises/{siren}")
def get_entreprise(siren: str):

    resultat = df[df["siren"] == siren]

    if resultat.empty:
        raise HTTPException(
            status_code=404,
            detail="Entreprise non trouvée"
        )

    entreprise = (
        resultat.iloc[0]
        .astype(object) #permite que las columnas puedan contener tipos más flexibles, incluido None.
        .where(pd.notna(resultat.iloc[0]),None) #donde el valor no sea NaN, mantenlo; donde el valor sea NaN, pon None.
        .to_dict()
    )
    
    return entreprise



