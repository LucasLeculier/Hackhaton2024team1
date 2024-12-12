import sys
import io

# Forcer l'encodage de sortie en UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

image_id = "booking_297_tabbar_withmenu@2x"

reponse_textuelle = """1. **Couleur dominante**
- Marron/terracotta comme fond de l'image principale
- Vert sage pour les �l�ments v�g�taux et le bouton "READ MORE"
- Blanc pour les textes et le bouton "BOOK NOW"
- Gris clair pour certains textes
- Bleu fonc� pour la barre de navigation

2. **Formes principales et taille des �l�ments**
- Image principale : occupe environ 30% de la hauteur
- Carte "About me" : occupe environ 25% de l'espace
- Boutons arrondis : "BOOK NOW" et "READ MORE"
- Barre de navigation : occupe 10% en bas
- Ic�nes de navigation : forme simple et minimaliste

3. **Layout**
- Structure verticale
- En-t�te avec le nom "Elysa Feigel"
- Section principale avec image et texte superpos�
- Carte "About me" centr�e
- Navigation fixe en bas
- Espacement �quilibr� entre les sections
- Alignement centr� des textes

4. **Style g�n�ral**
- Design �pur� et minimaliste
- Typographie moderne et l�g�re
- Approche professionnelle et zen
- Utilisation de superpositions textuelles sur l'image
- Style coh�rent et harmonieux

5. **Navigation**
- Barre fixe en bas de l'�cran
- 5 ic�nes de navigation
- Labels sous chaque ic�ne
- Design simple et intuitif
- Ic�nes : Home, Scheduling, Treatments, About me, Navigation

6. **Hi�rarchie visuelle**
1. Titre "Schedule an appointment"
2. Bouton "BOOK NOW"
3. Image principale
4. Section "About me"
5. Bouton "READ MORE"
6. Barre de navigation

Le design global est professionnel et bien structur�, avec une emphase claire sur la prise de rendez-vous et la pr�sentation des services."""


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

# Afficher les résultats
for feature, value in features.items():
    print(f"{feature} : {value}")

import mysql.connector

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Ton utilisateur MySQL
    password='',  # Ton mot de passe MySQL
    database='hackhaton2024'  # Le nom de ta base de données
)

cursor = conn.cursor()


print("image_id : " + image_id)
print("couleur dominante : " + features['Couleur dominante'])
print("formes principales et taille : " + features['Formes principales et taille des éléments'])
print("layout : " + features['Layout'])
print("style général : " + features['Style général'])
print("navigation : " + features['Navigation'])
print("hiérarchie visuelle : " + features['Hiérarchie visuelle'])





# Requête SQL pour insérer les données dans la table
insert_query = """
INSERT INTO design_features (image_id,couleur_dominante, formes_principales_et_taille, layout, style_general, navigation, hierarchie_visuelle)
VALUES (%s,%s, %s, %s, %s, %s, %s)
"""
data = (
    image_id,
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