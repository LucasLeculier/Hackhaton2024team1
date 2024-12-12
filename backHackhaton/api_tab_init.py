from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import json
import time
from anthropic import Anthropic

from openai import OpenAI

from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


openAIKey =  os.getenv("OPENAIKEY")
entropicKey = os.getenv("ENTROPICKEY")

app = FastAPI()

# Configuration de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (vous pouvez spécifier une liste comme ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les en-têtes
)
import mysql.connector
import json


def recuperer_data_user(cursor,tab):


    tab = ",".join(f"'{item}'" for item in tab)
    requete = f"""
    SELECT image_id, couleur, couleur_dominante, formes_principales_et_taille, layout, style_general, navigation, hierarchie_visuelle 
    FROM mobbin 
    WHERE image_id IN ({tab})
    """
    cursor.execute(requete)
    # Récupérer les résultats sous forme de tableau
    result = cursor.fetchall()
    # Initialiser une liste pour stocker les résultats
    tableau = []

    # Associé chaque résultat à un dictionnaire
    for row in result:
        image_data = {
            "image_id": row[0],
            "couleur": row[1],
            "couleur_dominante": row[2],
            "formes_principales_et_taille": row[3],
            "layout": row[4],
            "style_general": row[5],
            "navigation": row[6],
            "hierarchie_visuelle": row[7]
        }
        tableau.append(image_data)    

    # Convertir la liste de dictionnaires en JSON
    json_object = json.dumps(tableau, indent=4)
    return json_object
    



def fetch_data_gb(cursor):
    requete = "SELECT image_id, couleur, couleur_dominante, formes_principales_et_taille, layout, style_general, navigation, hierarchie_visuelle FROM design_features"
    cursor.execute(requete)

    result_gb = cursor.fetchall()

    tableau_gb = []

    for row in result_gb:
        image_data = {
            "image_id": row[0],
            "couleur": row[1],
            "couleur_dominante": row[2],
            "formes_principales_et_taille": row[3],
            "layout": row[4],
            "style_general": row[5],
            "navigation": row[6],
            "hierarchie_visuelle": row[7]
        }
        tableau_gb.append(image_data)    

    # Convertir la liste de dictionnaires en JSON
    json_gb = json.dumps(tableau_gb, indent=4)

    # Fermer la connexion
    cursor.close()
    
    return json_gb





import time
from anthropic import Anthropic
from openai import OpenAI


def requete_creation_meilleur_tuple(json_object):
    try:
        # Initialisation du client Anthropic (Claude)
        client_claude = Anthropic(api_key=entropicKey)
        claude_content = "voici des tuples de caractèristiques, ces plus tuples sont les design de web app que l'utilisateur aime, cependant je n'en veut qu'un au final. donc analyse l'ensemble des tuples pour en retourner un nouveau qui correspond aux gouts de l'user : " + json_object
        print("Requete 1 claude : "+str(len(claude_content)))
        # Envoi de la requête à Claude
        claude_response = client_claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": claude_content,
                }
            ],
        )

        # Vérification de la réponse de Claude
        reponse_textuelle = claude_response.content[0].text
        if "overloaded" not in reponse_textuelle.lower():
            return reponse_textuelle

    except Exception as e:
        print(f"Erreur avec Claude : {e}")

    # Si Claude échoue ou renvoie "overloaded", on utilise GPT
    try:
        # Initialisation du client OpenAI (GPT)
        client_gpt = OpenAI(api_key=openAIKey)
        gpt_content = "voici des tuples de caractèristiques, ces plus tuples sont les design de web app que l'utilisateur aime, cependant je n'en veut qu'un au final. donc analyse l'ensemble des tuples pour en retourner un nouveau qui correspond aux gouts de l'user : " + json_object
        print("Requete 1 gpt : "+str(len(gpt_content)))
        # Envoi de la requête à GPT
        gpt_response = client_gpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": gpt_content,
                }
            ]
        )

        # Extraction de la réponse textuelle
        reponse_textuelle = gpt_response.choices[0].message.content
        return reponse_textuelle

    except Exception as e:
        print(f"Erreur avec GPT : {e}")

    # Retourne une erreur si aucun modèle n'a pu répondre
    return "Erreur : Aucun modèle n'a pu traiter la requête."






def fetch_image_id(reponse_textuelle,json_gb):
    try:
        # Initialisation du client Anthropic (Claude)
        client_claude = Anthropic(api_key=entropicKey)

        claude_content = "voici des caractéristiques"+ reponse_textuelle +" retourne moi le tuple qui a le plus de similarité : " + json_gb + " la couleur est un critère véto, essayes de trouver une couleur qui se rapproche le + et retourne moi UNIQUEMENT 1 image_id qui correspond le + parmis tout les critères et dans ta réponse ne dit que l'image_id, rien d'autre"
        print("Requete 2 claude : "+str(len(claude_content)))
        # Envoi de la requête à Claude
        claude_response = client_claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": claude_content,
                }
            ],
        )

        # Vérification de la réponse de Claude
        reponse_textuelle = claude_response.content[0].text
        if "overloaded" not in reponse_textuelle.lower():
            return reponse_textuelle

    except Exception as e:
        print(f"Erreur avec Claude : {e}")

    # Si Claude échoue ou renvoie "overloaded", on utilise GPT
    try:
        # Initialisation du client OpenAI (GPT)
        client_gpt = OpenAI(api_key=openAIKey)

        gpt_content =  "voici des caractéristiques"+ reponse_textuelle +" retourne moi le tuple qui a le plus de similarité : " + json_gb + " la couleur est un critère véto, essayes de trouver une couleur qui se rapproche le + et retourne moi UNIQUEMENT 1 image_id qui correspond le + parmis tout les critères et dans ta réponse ne dit que l'image_id, rien d'autre"
        print("Requete 2 gpt : "+ str(len(gpt_content)))
        # Envoi de la requête à GPT
        gpt_response = client_gpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content":gpt_content,
                }
            ]
        )
        # Extraction de la réponse textuelle
        reponse_textuelle = gpt_response.choices[0].message.content
        return reponse_textuelle

    except Exception as e:
        print(f"Erreur avec GPT : {e}")

    # Retourne une erreur si aucun modèle n'a pu répondre
    return "Erreur : Aucun modèle n'a pu traiter la requête."



import mysql.connector
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def api_call(tab):
    def execute_with_timeout(func, *args, timeout=30):
        """Exécute une fonction avec un timeout."""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args)
            return future.result(timeout=timeout)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hackhaton2024"
        )

        # Gestion de la récupération des données utilisateur
        with conn.cursor() as cursor:
            try:
                json_object = execute_with_timeout(recuperer_data_user, cursor, tab, timeout=30)
            except TimeoutError:
                return {"error": "Timeout lors de la récupération des données utilisateur"}

        # Simulation d'une requête à GPT
        try:
            reponse_textuelle = execute_with_timeout(requete_creation_meilleur_tuple, json_object, timeout=30)
        except TimeoutError:
            return {"error": "Timeout lors de la génération de la réponse textuelle"}

        # Gestion de la récupération des données GB
        with conn.cursor() as cursor:
            try:
                json_gb = execute_with_timeout(fetch_data_gb, cursor, timeout=30)
            except TimeoutError:
                return {"error": "Timeout lors de la récupération des données GB"}

        # Trouver le meilleur tuple
        try:
            reponse_gpt = execute_with_timeout(fetch_image_id, reponse_textuelle, json_gb, timeout=30)
        except TimeoutError:
            return {"error": "Timeout lors de la recherche du meilleur tuple"}

        return reponse_gpt

    except mysql.connector.Error as e:
        return {"error": f"Erreur de connexion à la base de données : {e}"}

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


# Connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hackhaton2024"
    )

# Route API pour récupérer les données
@app.get("/fetch_tab")
def fetch_tab():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT image_id FROM mobbin LIMIT 10")
    result = cursor.fetchall()
    conn.close()

    tab = [row[0] for row in result]

    # Convertir le résultat en JSON et retourner
    return tab

"""
@app.get("/save_swiped_images")
def send_api_call(tab):
    print("tab : "+ tab)
    return api_call(tab)"""

@app.post("/save_swiped_images")

async def send_api_call(tab: str = Form(...)):
    retour = api_call(tab)
    return retour