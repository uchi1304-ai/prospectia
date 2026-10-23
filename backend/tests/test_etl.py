import pandas as pd
from app.etl import transform


def test_transform():

    df_test = pd.DataFrame([
        {
            "siren": "111111111",
            "nom": "Entreprise A",
            "secteur": "Transport",
            "effectif": 100,
            "chiffre_affaires": "100000",
            "ville": "paris"
        },
        {
            "siren": "111111111",
            "nom": "Entreprise A",
            "secteur": "Transport",
            "effectif": 100,
            "chiffre_affaires": "100000",
            "ville": "paris"
        },
        {
            "siren": "222222222",
            "nom": "Entreprise B",
            "secteur": "industrie",
            "effectif": -10,
            "chiffre_affaires": "unknown",
            "ville": "lyon"
        }
    ])

    resultat = transform(df_test)

    # print("\nRESULTAT:")
    # print(resultat)

    # print(
    #     "Duplicados:",
    #     resultat["siren"].duplicated().sum()
    # )

    # print(
    #     "Effectifs negativos:",
    #     (resultat["effectif"] < 0).sum()
    # )

    # print(
    #     "NaN totales:",
    #     resultat.isna().sum().sum()
    # )

    assert resultat["siren"].duplicated().sum() == 0
    assert (resultat["effectif"] < 0).sum() == 0
    assert resultat.isna().sum().sum() == 0

    assert "Paris" in resultat["ville"].values
    assert "Transport" in resultat["secteur"].values
    assert "Industrie" in resultat["secteur"].values

    assert resultat.loc[
        resultat["siren"] == "222222222",
        "chiffre_affaires"
    ].iloc[0] == 100000

