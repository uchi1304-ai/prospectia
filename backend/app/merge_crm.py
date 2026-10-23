import pandas as pd

df_externe = pd.read_csv(
    "data/entreprises_clean.csv", 
    dtype={"siren": str}
)

df_crm = pd.read_csv(
    "data/crm_interne.csv",
    dtype={"siren": str}
) 

df_final = df_externe.merge(
    df_crm,
    on="siren",
    how="left"
)

print(df_externe.shape)    
print(df_crm.shape)
print (df_final.shape)
print(df_final.head())
print(df_final["ancien_client"].isna().sum())


df_avec_crm = df_final[
    df_final["opportunite"].notna()
].copy()

df_sans_crm = df_final[
    df_final["opportunite"].isna()
].copy()


print(df_avec_crm.shape)
print(df_sans_crm.shape)

df_avec_crm.to_csv(
    "data/dataset_ml.csv",
    index=False
)