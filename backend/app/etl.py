import requests
import pandas as pd

def extract(): 

    df_sirens = pd.read_csv("data/sirens_a_consulter.csv", 
    dtype= {"siren": str}
    )

    entreprises = []
    erreurs = []

    for siren in df_sirens["siren"]: 
        url = f"http://127.0.0.1:8000/entreprises/{siren}"

        response = requests.get(url)

        if response.status_code ==200: 

            data = response.json()
            entreprises.append(data)

        else:

            erreurs.append({
                "siren":siren, 
                "status_code": response.status_code
            })

    df_entreprises = pd.DataFrame(entreprises)
    df_erreurs = pd.DataFrame(erreurs)

    return df_entreprises, df_erreurs

  
# df_entreprises, df_erreurs = extract()
# # dame lo que sacaste de la función y guárdamelo aquí para poder seguir usándolo

# print(df_entreprises.shape)
# print(df_erreurs.shape)


def transform(df): 

    df = df.copy()

    df = df.drop_duplicates()

    df["chiffre_affaires"]= pd.to_numeric(
        df["chiffre_affaires"], 
        errors= "coerce"
)
    df.loc[df["effectif"]<0, "effectif"]= pd.NA
    df.loc[df["chiffre_affaires"]<0,"chiffre_affaires"] = pd.NA

    df["nom"] = df["nom"].str.strip()
    df["secteur"] = df["secteur"].str.strip()
    df["ville"] = df["ville"].str.strip()

    df["secteur"]= df["secteur"].str.capitalize()
    df["ville"]= df["ville"].str.title()

    df.loc[df["secteur"] == "Non renseigné", "secteur"]= pd.NA
    df.loc[df["ville"] == "Inconnue", "ville"]= pd.NA
    df.loc[df["nom"] == "À compléter", "nom"]= pd.NA

    df["effectif"]= df["effectif"].fillna(
        df["effectif"].median()
    )

    df["chiffre_affaires"] = df["chiffre_affaires"].fillna(
        df["chiffre_affaires"].median()
    )

    df["secteur"] = df["secteur"].fillna("Inconnu")
    df["ville"] = df["ville"].fillna("Inconnue")

    df = df.dropna(subset=["nom"])

    return df

# df_clean = transform(df_entreprises)

# print(df_clean.shape)
# print(df_clean.isna().sum())
# print(df_clean.duplicated().sum())

def load (df_clean, df_erreurs): 

    df_clean.to_csv("data/entreprises_clean.csv", 
    index=False
    )

    df_erreurs.to_csv("data/erreurs_extraction.csv",
                      index=False
                      )


def main(): 

    df_entreprises, df_erreurs = extract()

    df_clean = transform(df_entreprises)

    load(df_clean, df_erreurs)

if __name__ == "_main_":
    main()