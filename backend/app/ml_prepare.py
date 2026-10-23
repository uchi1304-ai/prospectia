import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score, 
    recall_score, 
    f1_score, 
    confusion_matrix
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib 
import os


df = pd.read_csv(
    "data/dataset_ml.csv",
    dtype={"siren":str}
    )

X = df[
    [
        "effectif", 
        "chiffre_affaires",
        "secteur", 
        "ville",
        "ancien_client",
        "consommation", 
        "nb_contacts"
    ]
]

y = df["opportunite"]

# print(X.head())
# print(y.head())
# print(X.shape)
# print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y, 
    test_size=0.2,#20% para prueba 
    random_state=42, #simepre se obtendra la misma separacion de empresas
    stratify=y #para que el train y el test tengan la misma proporcion de oportunidades
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

colonnes_categoriques = [
    "secteur", 
    "ville"
] 

colonnes_numeriques = [
    "efffectif", 
    "chiffre_affaires", 
    "ancien_client", 
    "consommation", 
    "nb_contacts"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat", #nombre de la transformacion
            OneHotEncoder(handle_unknown="ignore"), #que transformacion quiero hacer si no conzco alguna que no estuvo en train lo ignoro en test y sigo 
            colonnes_categoriques #sobre que columnas 
        )
    ],
    remainder="passthrough" #el resto dejalo pasar 
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))#nombre classidifer y modelo que quiero usar aqui le dices que haga 1000 iteraciones max 
    ]
)

model.fit(X_train, y_train)#entranamiento del modelo 

y_pred = model.predict(X_test) #tomas las que deje aparte y dime que predices para esas empresas 

print(y_pred[:20]) #imprime las 20 primeras predicciones 
print(y_test.head(20).values) #primeros 20 valores reales de y test 


accuracy = accuracy_score(y_test, y_pred) #cuantas  acerto de todas las predicciones
precision = precision_score(y_test, y_pred) #cuantas veces tuvo razon cuando dijo que es oportunidad
recall = recall_score(y_test, y_pred) #de todas las oportunidades reales, cuantas logro detectar
f1 = f1_score(y_test, y_pred)#eauilibrio entre precision y recall 

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

print("Matrice de confusion:")
print(confusion_matrix(y_test,y_pred))


score_logistic = cross_val_score(
    model,
    X_train, 
    y_train,
    cv=5,
    scoring="recall"
)

print ("Recall Logistica por fold:", score_logistic)
print("Recall Logistic moyen:", score_logistic.mean())



model_rf= Pipeline(
    steps=[
        ("processor", preprocessor),
        (
            "classifier", 
            RandomForestClassifier(
                n_estimators=100, #numero de arboles de decision
                random_state=42 
            )
        )
    ]
)


model_rf.fit(X_train, y_train)

y_pred_rf= model_rf.predict(X_test)

accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf)
recall_rf = recall_score(y_test, y_pred_rf)
f1_rf = f1_score(y_test, y_pred_rf)

print("Random Forest")
print("Accuracy :", accuracy_rf)
print("Precision :", precision_rf)
print("Recall :", recall_rf)
print("F1 :", f1_rf)

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred_rf))

score_rf = cross_val_score(
    model_rf, 
    X_train,
    y_train, 
    cv=5,
    scoring="recall"
)

print("Recall Random Forest por fold:", score_rf)
print("Recall Random Forest moyen:", score_rf.mean())

os.makedirs("models", exist_ok=True) #crea una carpeta para los modelos 

joblib.dump (model,"models/prospectia_model.pkl")#guarda el pipeline en el archivo 
