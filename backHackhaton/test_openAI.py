

from anthropic import Anthropic
client = Anthropic(
    api_key="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"
)

import base64
import httpx
from colorthief import ColorThief

Prompt = """Vous êtes un expert en design et analyse d'images. Voici une image encodée en base64. Analysez cette image selon les critères suivants et fournissez les informations détaillées en suivant cette structure :
1. **Couleur dominante** : Listez les couleurs principales de l'image, y compris les nuances de chaque couleur (par exemple, marron/terracotta, vert, blanc).
2. **Formes principales et taille des éléments** : Décrivez les formes des éléments principaux dans l'image, comme les boutons, les cartes, l'image principale, etc. Indiquez également la taille relative de chaque élément (par exemple, l'image principale occupe 40% de l'espace).
3. **Layout** : Décrivez la structure générale de la page, y compris la disposition des sections (par exemple, en-tête, section principale, barre de navigation, etc.), ainsi que l'alignement des éléments (centré, aligné à gauche, etc.). Mentionnez aussi l'utilisation de l'espace blanc.
4. **Style général** : Donnez une description du style visuel général de l'image (par exemple, moderne, minimaliste, professionnel). Précisez les éléments notables comme la typographie ou l'approche générale du design.
5. **Navigation** : Décrivez la barre de navigation et son placement, ainsi que les éléments de navigation, tels que les icônes et les textes associés. Indiquez également le style de la navigation (par exemple, fixe, contrastée).
6. **Hiérarchie visuelle** : Listez les éléments selon leur priorité visuelle (par exemple, le titre principal, le bouton CTA, l'image, etc.), en mentionnant ce qui attire le plus l'attention.

Répondez en suivant exactement cette structure. Utilisez des listes et des sous-sections pour chaque critère et fournissez des détails spécifiques pour chaque élément analysé.
"""


# Fonction pour convertir une image en base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Fonction pour analyser la couleur dominante localement
def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)  # Renvoie un tuple (R, G, B)
    return dominant_color

# Préparer l'image
image_path = "../webp/booking_231_floatingtabbar_withmenu@2x.webp"
image_base64 = image_to_base64(image_path)
dominant_color = get_dominant_color(image_path)
image_media_type = "image/webp"
image_name = image_path.split("/")[-1]
image_id = image_name


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

hex_code = rgb_to_hex(dominant_color)


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

#print(reponse_textuelle)


import re

# Fonction pour extraire les données spécifiques
def extract_features(response):
    features = {}

    # Regex pour chaque critère
    match_couleur_dominante = re.search(r"1\. \*\*Couleur dominante\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_couleur_dominante:
        features['Couleur dominante'] = match_couleur_dominante.group(1).strip()
    else:
        features['Couleur dominante'] = "Non trouvée"

    match_formes = re.search(r"2\. \*\*Formes principales et taille des éléments\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_formes:
        features['Formes principales et taille des éléments'] = match_formes.group(1).strip()
    else:
        features['Formes principales et taille des éléments'] = "Non trouvée"

    match_layout = re.search(r"3\. \*\*Layout\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_layout:
        features['Layout'] = match_layout.group(1).strip()
    else:
        features['Layout'] = "Non trouvé"

    match_style = re.search(r"4\. \*\*Style général\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_style:
        features['Style général'] = match_style.group(1).strip()
    else:
        features['Style général'] = "Non trouvé"

    match_navigation = re.search(r"5\. \*\*Navigation\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_navigation:
        features['Navigation'] = match_navigation.group(1).strip()
    else:
        features['Navigation'] = "Non trouvé"

    match_hierarchie = re.search(r"6\. \*\*Hiérarchie visuelle\*\*[\s\S]*?:\s*([\s\S]*?)(?=\n\n|$)", response)
    if match_hierarchie:
        features['Hiérarchie visuelle'] = match_hierarchie.group(1).strip()
    else:
        features['Hiérarchie visuelle'] = "Non trouvée"

    return features


# Extraire les données
features = extract_features(reponse_textuelle)

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
INSERT INTO design_features (image_id,couleur,couleur_dominante, formes_principales_et_taille, layout, style_general, navigation, hierarchie_visuelle)
VALUES (%s,%s,%s, %s, %s, %s, %s, %s)
"""
data = (
    image_id,
    hex_code,
    features['Couleur dominante'],
    features['Formes principales et taille des éléments'],
    features['Layout'],
    features['Style général'],
    features['Navigation'],
    features['Hiérarchie visuelle']
)

# Exécution de la requête d'insertion
cursor.execute(insert_query, data)

# Commit des modifications
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()


print("Les données ont été insérées avec succès dans la base de données.")