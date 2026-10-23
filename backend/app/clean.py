import pandas as pd


df = pd.read_csv("data/entreprises_extraites.csv", 
                dtype={"siren":str}
)

print(df.head())
print(df.shape)
df.info()

print("\nVALEURS MANQUANTES")
print(df.isna().sum())

print("\nDOUBLONS SIREN")
print(df["siren"].duplicated().sum())

print("\nEXEMPLE DE SIREN DUPLIQUES")

duplicates = df[df["siren"].duplicated(keep=False)]

print(
    duplicates
    .sort_values("siren") #ordenalos por siren
    .head(20) #dame los primeros 20
)

print("\nDOUBLONS EXACTS")
print(df.duplicated().sum())

#1. ELIMINATION DE DOUBLONS
df = df.drop_duplicates()
print(df.shape)
print(df.duplicated().sum())

#2. cambiar los valores de chiffre de affaires a numericos 
df["chiffre_affaires"] = pd.to_numeric(
    df["chiffre_affaires"],
    errors="coerce" #si un valor no puede convertirse a número, conviértelo en NaN
)

# print(df.info())
# print(df.isna().sum())

# Detectemos valores numéricos imposibles o sospechoso
print("\nEFFECTIF NEGATIFS")
print (
    df[df["effectif"]<0]
    [["siren","effectif"]]
    .head(20))

print("\nCHIFFRE AFFAIRES NEGATIF")
print(
    df[df["chiffre_affaires"]<0]
    [["siren","chiffre_affaires"]]
    .head(20)
)

#3. CONVERTIR NEGATIVOS EN NaN
df.loc[df["effectif"]<0,"effectif"]=pd.NA
df.loc[df["chiffre_affaires"]<0,"chiffre_affaires"]= pd.NA


# df.loc[condicion, "columna"]
# selecciona las filas que cumplen esa condición, pero solo en esa columna y reemplazalo por valor faltante.

# print(df.isna().sum())

#revision de texto unico 
print("\nSECTEURS UNIQUES")
print(df["secteur"].value_counts(dropna=False).head(30))

print("\nVILLES UNIQUES")
print(df["ville"].value_counts(dropna=False).head(30))
#cuenta los valores distintos de la columna incluidos los na 

print("\nNOM SUSPECTS")
print(
    df[
        df["nom"].str.contains(
            "compléter",
            case=False,
            na=False
        )
    ][["siren", "nom"]].head(20)
)
# primeras 20 filas donde el nombre contiene “compléter”, sin importar mayúsculas/minúsculas, 
# y muéstrame solo el SIREN y el nombre.

# 4. LIMPIAMOS ESPACIOS 
df["nom"]= df["nom"].str.strip()
df["secteur"]= df["secteur"].str.strip()
df["ville"]= df["ville"].str.strip()

# 5. NORMALIZAMOS MAYUS Y MINUS 
df["secteur"] = df["secteur"].str.capitalize()
df["ville"] = df["ville"].str.title()

# 6. CONVERTIMOS FALSOS VALORES EN VERDADEROS NULOS 
df.loc[df["secteur"] == "Non renseigné", "secteur"] = pd.NA
df.loc[df["ville"] == "Inconnue", "ville"] = pd.NA
df.loc[df["nom"] == "À compléter", "nom"] = pd.NA


# print("\nVALEURS MANQUANTES APRÈS NETTOYAGE")
# print(df.isna().sum())

# print("\nSECTEURS APRÈS NORMALISATION")
# print(df["secteur"].value_counts(dropna=False))

# print("\nVILLES APRÈS NORMALISATION")
# print(df["ville"].value_counts(dropna=False))


# nom
# → si falta, la fila pierde una información básica de identificación comercial
# → mejor eliminar esas filas
df = df.dropna(subset=["nom"])


# secteur
# → si falta, podríamos conservar la empresa, pero marcarla como "Inconnu"
# → porque puede seguir siendo útil

# ville
# → igual: conservar y poner "Inconnue"

df["secteur"] = df["secteur"].fillna("Inconnu")
df["ville"] = df["ville"].fillna("Inconnue")

# effectif
# → no conviene inventar un número al azar
# → podemos imputar con la mediana

# chiffre_affaires
# → también podemos imputar con la mediana
# print("\nMEDIANE EFFECTIF")
# print(df["effectif"].median())

# print("\nMEDIANE CHIFFRE AFFAIRES")
# print(df["chiffre_affaires"].median())

df["effectif"] = df["effectif"].fillna(
    df["effectif"].median()
)

df["chiffre_affaires"] = df["chiffre_affaires"].fillna(
    df["chiffre_affaires"].median()
)

print(df.isna().sum())
print(df.shape)

print("\n=====================")
print("\nVALIDATION FINALE")
print("\n=====================")

print("Doublons:", df.duplicated().sum())

print(
    "Effectifs négatifs:",
    (df["effectif"] < 0).sum()
)

print(
    "CA négatifs:",
    (df["chiffre_affaires"] < 0).sum()
)

print("\nTYPES")
print(df.dtypes)

df.to_csv(
    "data/entreprises_clean.csv",
    index=False
)