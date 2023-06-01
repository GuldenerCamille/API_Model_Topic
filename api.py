# Import des librairies
import mysql.connector
from fastapi import FastAPI
import os
from urllib.parse import urlparse
from model import label_topic
# ============================================== UTILITAIRES ==================================================>

# Pour lancer l'application et l'API

# 1) execute => uvicorn api:app --reload.
# 2) execute => run streamlit main.py.

# Initialisation de l'app FastAPI/connexion BDD.
app = FastAPI()


def connect():
    cnx = mysql.connector.connect(
        user="ahmed",
        password="Flight_delay",
        host="ahmedsakserver.mysql.database.azure.com",
        port=3306,
        database="nlp_topic",
        ssl_disabled=False
    )
    return cnx

# ================================ REQUETES SQL =================================>

# Fonction permettant d'insérer les données.
def insert_data_to_database(data, table, connexion):
    try:
        cursor = connexion.cursor()
        table1_sql = f"INSERT INTO {table} (abstract, topic_prediction) VALUES (%s, %s)"
        cursor.execute(table1_sql, (data["feature"], data["prediction"]))
        connexion.commit()
        cursor.close()
    except Exception as e:
        print(e)
        
# Fonction pour récupérer les données depuis la base de données MySQL.
def get_data_from_database(table, connexion):
    cursor = connexion.cursor()   
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    connexion.close()
    return data

# Fonction pour supprimer les données depuis la base de données MySQL.
def delete_data_from_database(table, connexion):
    cursor = connexion.cursor()
    cursor.execute(f"DELETE FROM {table}")
    connexion.commit()
    connexion.close()
    
# ================================ END POINT ====================================>

# Route pour envoyer des données via une requête POST (before).
@app.post("/data/post")
async def send_data(data: dict):
    connexion = connect()
    
    
    # On réalise la prédiction (faire les modifications ici)
    prediction = label_topic(data["feature"])
    data["prediction"] = str(prediction)
    
    
    insert_data_to_database(data=data, table="nlp_topic", connexion=connexion)
    connexion.close()
    return

# ===============================================================================>

# Route pour récupérer les données via une requête GET (before).
@app.get("/data/get")
async def get_data():
    connexion = connect()
    data = get_data_from_database(
        table="nlp_topic", 
        connexion=connexion
    )
    connexion.close()
    return {"data": data}

# Fonction pour supprimer toutes les données.
@app.delete("/data/delete")
async def delete_data():
    connexion = connect()
    delete_data_from_database(
        table="nlp_topic",
        connexion=connexion
    )
    connexion.close()
    return "Données supprimées avec succès."