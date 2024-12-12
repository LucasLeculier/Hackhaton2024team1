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





def requete_creation_meilleur_tuple(json_object):

    from anthropic import Anthropic

    client = Anthropic(
        api_key="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"
    )


    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "voici des tuples de caractèristiques, ces plus tuples sont les design de web app que l'utilisateur aime, cependant je n'en veut qu'un au final. donc analyse l'ensemble des tuples pour en retourner un nouveau qui correspond aux gouts de l'user : " + json_object
                    }
                ],
            }
        ],
    )

    reponse_textuelle = message.content[0].text
    return reponse_textuelle



from openai import OpenAI

def fetch_image_id(reponse_textuelle,json_gb):

    client = OpenAI(
    api_key="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"
)
    

    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": "voici des caractéristiques"+ reponse_textuelle +" retourne moi le tuple qui a le plus de similarité : " + json_gb + " la couleur est un critère véto, essayes de trouver une couleur qui se rapproche le + et retourne moi UNIQUEMENT 1 image_id qui correspond le + parmis tout les critères et dans ta réponse ne dit que l'image_id, rien d'autre",
        }],
        model="gpt-4o-mini",
    )

    reponse_gpt = response.choices[0].message.content

    return reponse_gpt



def api_call(tab):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hackhaton2024"
        )

        # Gestion de la récupération des données utilisateur
        with conn.cursor() as cursor:
            json_object = recuperer_data_user(cursor,tab)

        # Simulation d'une requête à GPT
        reponse_textuelle = requete_creation_meilleur_tuple(json_object)

        # Gestion de la récupération des données GB
        with conn.cursor() as cursor:
            json_gb = fetch_data_gb(cursor)

        # Trouver le meilleur tuple
        reponse_gpt = fetch_image_id(reponse_textuelle, json_gb)

        return reponse_gpt

    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
    finally:
        if conn.is_connected():
            conn.close()



tab= ['image_1.jpg','image_32.jpg','image_39.jpg','image_62.jpg','image_65.jpg']  



print(api_call(tab))          