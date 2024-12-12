import os
import shutil

# Chemin vers le dossier source contenant les images
source_folder = r'../webp'

# Chemin vers le dossier de destination
destination_folder = r'../webp/trier'

# Créer le dossier de destination s'il n'existe pas
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Parcourir tous les fichiers dans le dossier source
for filename in os.listdir(source_folder):
    # Vérifier si le fichier contient "floatingtabbar" dans son nom
    if "floatingtabbar" in filename.lower():
        # Définir le chemin complet des fichiers source et destination
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
        
        # Copier le fichier dans le dossier de destination
        shutil.copy(source_file, destination_file)
        print(f"Copié : {filename}")

print("Copie terminée.")
