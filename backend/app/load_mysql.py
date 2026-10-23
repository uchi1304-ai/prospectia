import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


df= pd.read_csv(
    "data/entreprises_clean.csv", 
    dtype={"siren": str}
    )


connexion = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
    use_pure=True
)

cursor = connexion.cursor()# python envie ordenes a sql a mysql 

secteurs = df["secteur"].unique()
villes = df["ville"].unique()

for secteur in secteurs: 

    cursor.execute(
        """
        INSERT IGNORE INTO SECTEUR (nom_secteur)
        VALUES (%s)
        """, 
        (secteur,)
    )


for ville in villes:

    cursor.execute(
        """
        INSERT IGNORE INTO VILLE (nom_ville)
        VALUES (%s)
        """,
        (ville,)
    )


for _, row in df.iterrows():
#recorre cada fila del daatafrrame

    cursor.execute(
        """
        SELECT id_secteur
        FROM SECTEUR 
        WHERE nom_secteur = %s
        """,
        (row["secteur"],)
    )

    id_secteur = cursor.fetchone()[0]
    #recupera una sola fial del resultado 
    cursor.execute(
        """
        SELECT id_ville
        FROM VILLE
        WHERE nom_ville = %s
        """,
        (row["ville"],)
    )

    id_ville = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT IGNORE INTO ENTREPRISE(
        siren, 
        nom,
        effectif,
        chiffre_affaires,
        id_secteur, 
        id_ville
        
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            row["siren"],
            row["nom"],
            int(row["effectif"]),
            float(row["chiffre_affaires"]),
            id_secteur,
            id_ville 
        )
    )

connexion.commit()

print("Secteurs insérés avec succès")

cursor.close()
connexion.close()