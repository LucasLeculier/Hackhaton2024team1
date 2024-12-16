from anthropic import Anthropic
client = Anthropic(
    api_key="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"
)
import json
import base64
import httpx
from colorthief import ColorThief

Prompt = """You are an expert in design and image analysis. Below is an image encoded in Base64. Analyze this image based on the following criteria and provide detailed information in this structured JSON format:  

json:  
{  
  "DominantColor": {  
    "Theme": "Dark" | "Light"  
  },  
  "PrimaryShapesAndElementSizes": [  
    {  
      "Shape": "string",  
      "Description": "string",  
      "RelativeSizePercentage": "number"  
    }  
  ],  
  "Layout": {  
    "GeneralStructure": "string",  
    "ElementAlignment": "string",  
    "WhitespaceUtilization": "string"  
  },  
  "GeneralStyle": {  
    "Category": "E-commerce" | "Social Media" | "Activities" | "Food and Restaurants"  
  },  
  "Navigation": {  
    "Placement": "string",  
    "VisualElements": ["string"],  
    "Style": "string"  
  },  
  "VisualHierarchy": [  
    {  
      "Element": "string",  
      "Priority": "number",  
      "Reason": "string"  
    }  
  ]  
}
"""


    
# Fonction pour convertir une image en base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

import os
#folder_path = "../webp/trier"

folder_path = "activite"



files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

print(files)

# Traitement des fichiers
for file in files:
    image_path = os.path.join(folder_path, file)
    image_base64 = image_to_base64(image_path)
    image_name = file
    image_id = image_name  # Utiliser le nom du fichier comme ID
    #get extension of image
    extension = os.path.splitext(image_path)[1]
    if(extension == ".png"):
        image_media_type = "image/png"
    if(extension == ".jpg"):
        image_media_type = "image/webp"


    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": Prompt
                    }
                ],
            }
        ],
    )
    reponse_textuelle = message.content[0].text

    print("réponse claude recue")

   
    # Charger la chaîne JSON dans un dictionnaire
    parsed_data = json.loads(reponse_textuelle)

    # Construire les variables sous forme de chaînes concaténées
    DominantColor_Theme = f"Theme: {parsed_data['DominantColor']['Theme']}"

    PrimaryShapesAndElementSizes = " | ".join([
        f"Shape: {item['Shape']}, Description: {item['Description']}, RelativeSizePercentage: {item['RelativeSizePercentage']}%"
        for item in parsed_data['PrimaryShapesAndElementSizes']
    ])

    Layout = f"GeneralStructure: {parsed_data['Layout']['GeneralStructure']} | " \
            f"ElementAlignment: {parsed_data['Layout']['ElementAlignment']} | " \
            f"WhitespaceUtilization: {parsed_data['Layout']['WhitespaceUtilization']}"

    GeneralStyle_Category = f"Category: {parsed_data['GeneralStyle']['Category']}"

    Navigation = f"Placement: {parsed_data['Navigation']['Placement']} | " \
                f"VisualElements: {', '.join(parsed_data['Navigation']['VisualElements'])} | " \
                f"Style: {parsed_data['Navigation']['Style']}"

    VisualHierarchy = " | ".join([
        f"Element: {item['Element']}, Priority: {item['Priority']}, Reason: {item['Reason']}"
        for item in parsed_data['VisualHierarchy']
    ])

    import mysql.connector

    # Connexion à la base de données MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Ton utilisateur MySQL
        password='',  # Ton mot de passe MySQL
        database='hackhaton2024'  # Le nom de ta base de données
    )
    cursor = conn.cursor()
    # Requête SQL pour insérer les données dans la table
    insert_query = """
    INSERT INTO mobbin_bak (image_id,DominantColor, PrimaryShapesAndElementSizes,Layout, GeneralStyle,Navigation, VisualHierarchy,numero_set)
        VALUES (%s,%s,%s, %s, %s, %s, %s,4)
    """
    data = (
        image_id,
        DominantColor_Theme,
        PrimaryShapesAndElementSizes,
        Layout,
        GeneralStyle_Category,
        Navigation,
        VisualHierarchy

    )

    # Exécution de la requête d'insertion
    cursor.execute(insert_query, data)

    # Commit des modifications
    conn.commit()

    # Fermer la connexion
    cursor.close()
    conn.close()


    print("Les données ont été insérées avec succès dans la base de données.")