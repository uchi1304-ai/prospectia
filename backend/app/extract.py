import requests
import pandas as pd


df_sirens = pd.read_csv(
    "data/sirens_a_consulter.csv",
    dtype={"siren":str}
)

entreprises = []
erreurs = []

for siren in df_sirens["siren"]:
# recorre uno por uno todos los valores de la columna siren.
    
    url = f"http://127.0.0.1:8000/entreprises/{siren}"

    response = requests.get(url)

    if response.status_code == 200: 
        data = response.json()
        # cambialo a diccionario python
        entreprises.append(data)

    else: 
        erreurs.append({
            "siren": siren, 
            "status_code": response.status_code
            })

df_entreprises = pd.DataFrame(entreprises)
df_erreurs = pd.DataFrame(erreurs)
# conviertelo en tabla, creamos dataframe 
 


df_entreprises.to_csv(
    "data/entreprises_extraites.csv", 
    index=False
)

df_erreurs.to_csv(
    "data/erreurs_extraction.csv", 
    index=False
)

# guardamos la tabla en un csv sin indice 