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

# Liste des origines autorisées (ici '*' pour toutes les origines)
origins = [
    "*",  # Autorise toutes les origines (à remplacer par une liste spécifique si nécessaire)
]




def recuperer_data_user(cursor,tab):

    tab = tab.split(",")

    tab_sql = ""
    for element in tab:
        tab_sql += element+","

    #enelever les [ ] de la chaine
    tab_sql = tab_sql[1:-1]
    tab_sql = tab_sql[:-1]

    # Construire la requête SQL
    requete = f"""
    SELECT * from mobbin_bak
    WHERE image_id IN ({tab_sql})
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
            "DominantColor": row[1],
            "PrimaryShapesAndElementSizes": row[2],
            "Layout": row[3],
            "GeneralStyle": row[4],
            "Navigation": row[5],
            "VisualHierarchy": row[6]
        }
        tableau.append(image_data)    

    # Convertir la liste de dictionnaires en JSON
    json_object = json.dumps(tableau, indent=4)
    return json_object
    



def fetch_data_gb(cursor,reponse_textuelle):
    print("reponse_textuelle : "+reponse_textuelle)

    #if reponse_textuelle contains "E-commerce"
    if "E-commerce" in reponse_textuelle:
        categorie = "E-commerce"
    elif "Social Media" in reponse_textuelle:
        categorie = "Social Media"
    elif "Food and Restaurants" in reponse_textuelle:
        categorie = "Food and Restaurants"
    else :
        categorie = "Activities"    

    if "Theme: Dark" in reponse_textuelle:
        theme = "Dark"
    else :
        theme = "Light"

    print("categorie : "+categorie)
    print("theme : "+theme)    
    #ICIIII Récupérer la catégorie via le json
    requete = "SELECT * FROM design_features_bak where GeneralStyle like '%"+categorie+"%';"


    cursor.execute(requete)

    result_gb = cursor.fetchall()

    tableau_gb = []

    for row in result_gb:
        image_data = {
            "image_id": row[0],
            "DominantColor": row[1],
            "PrimaryShapesAndElementSizes": row[2],
            "Layout": row[3],
            "GeneralStyle": row[4],
            "Navigation": row[5],
            "VisualHierarchy": row[6]
        }
        tableau_gb.append(image_data)    

    # Convertir la liste de dictionnaires en JSON
    json_gb = json.dumps(tableau_gb, indent=4)

    # Fermer la connexion
    cursor.close()
    
    return json_gb, categorie, theme





import time
from anthropic import Anthropic
from openai import OpenAI


def requete_creation_meilleur_tuple(json_object):
    try:
        # Initialisation du client Anthropic (Claude)
        client_claude = Anthropic(api_key=entropicKey)
        claude_content = """
        Below are tuples representing the characteristics of web app designs that the user likes. Your task is to analyze all these tuples and return a single new tuple that best matches the user's preferences. When creating the final tuple, prioritize the importance of the criteria as follows:
        1- Category and Theme Color are the most important factors and should be considered first.
        2 -The remaining characteristics should then be factored in to refine the final design.
        Make sure the resulting tuple reflects the user's overall tastes.
        """+json_object
        
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
        gpt_content = """
        Below are tuples representing the characteristics of web app designs that the user likes. Your task is to analyze all these tuples and return a single new tuple that best matches the user's preferences. When creating the final tuple, prioritize the importance of the criteria as follows:
        1- Category and Theme Color are the most important factors and should be considered first.
        2 -The remaining characteristics should then be factored in to refine the final design.
        Make sure the resulting tuple reflects the user's overall tastes.
        """+json_object
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

        claude_content = "Here are some characteristics: "+reponse_textuelle+". Return the tuple that has the highest similarity to these characteristics: "+json_gb+""".

Prioritize the criteria as follows:

Category and Theme Color are the most important and should be considered first. Try to find a theme color that closely matches the preferences.
Consider the remaining characteristics to further refine the selection.
Return only one image_id that best matches all the criteria. In your response, provide only the image_id and nothing else.
"""
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

        gpt_content =   "Here are some characteristics: "+reponse_textuelle+". Return the tuple that has the highest similarity to these characteristics: "+json_gb+""".

Prioritize the criteria as follows:

Category and Theme Color are the most important and should be considered first. Try to find a theme color that closely matches the preferences.
Consider the remaining characteristics to further refine the selection.
Return only one image_id that best matches all the criteria. In your response, provide only the image_id and nothing else.
"""
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
                json_gb,categorie,theme = execute_with_timeout(fetch_data_gb, cursor,reponse_textuelle, timeout=30)
            except TimeoutError:
                return {"error": "Timeout lors de la récupération des données GB"}
        # Trouver le meilleur tuple
        try:
            reponse_gpt = execute_with_timeout(fetch_image_id, reponse_textuelle, json_gb, timeout=30)
        except TimeoutError:
            return {"error": "Timeout lors de la recherche du meilleur tuple"}
        return reponse_gpt,categorie,theme

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
    cursor.execute("SELECT image_id FROM mobbin_bak where numero_set=0;")
    result = cursor.fetchall()
    conn.close()

    tab = [row[0] for row in result]


    # Convertir le résultat en JSON et retourner
    return tab

@app.get("/fetch_tab_affiner")
async def fetch_tab(categorie: str, theme: str):

    if(categorie == "E-commerce"):
        numero_set = 2
    elif(categorie == "Social Media"):
        numero_set = 3
    elif(categorie == "Food and Restaurants"):
        numero_set = 1    
    else:
        numero_set = 4
    conn = get_db_connection()
    cursor = conn.cursor()
    requete = "SELECT image_id FROM mobbin_bak where numero_set="+str(numero_set)+";"
    cursor.execute(requete)
    result = cursor.fetchall()
    conn.close()

    tab = [row[0] for row in result]

    # Convertir le résultat en JSON et retourner
    print("tab affiné : "+str(tab))
    return tab

"""
@app.get("/save_swiped_images")
def send_api_call(tab):
    print("tab : "+ tab)
    return api_call(tab)"""

@app.post("/save_swiped_images")
async def send_api_call(tab: str = Form(...)):
    retour,theme,cat = api_call(tab)
    print("retour : "+str(retour))
    return retour,theme,cat