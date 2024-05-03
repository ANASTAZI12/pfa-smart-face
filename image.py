import cv2
import os
import time

# Modèle de nom pour les groupes d'images
nom_modele = "groupe_{}"

# Répertoire de sortie pour stocker les captures de visages
output_directory = "captures_visages"

# Créer le répertoire s'il n'existe pas
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Créer un objet VideoCapture pour accéder à la webcam
cap = cv2.VideoCapture(0)  # 0 pour la webcam par défaut

# Charger le détecteur de visage Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Vérifier si la webcam est ouverte correctement
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

# Compteur pour nommer les groupes d'images
groupe_count = 1

# Lire les images de la webcam en continu
while True:
    # Générer un nom pour ce groupe d'images
    nom_groupe = nom_modele.format(groupe_count)

    # Créer un sous-répertoire pour ce groupe d'images
    groupe_directory = os.path.join(output_directory, nom_groupe)
    if not os.path.exists(groupe_directory):
        os.makedirs(groupe_directory)

    # Compteur pour nommer les images capturées dans ce groupe
    image_count = 0

    # Lire les images de la webcam en continu pour ce groupe
    while True:
        # Lire un frame depuis la webcam
        ret, frame = cap.read()

        # Vérifier si la lecture du frame est réussie
        if not ret:
            print("Erreur: Impossible de lire le frame.")
            break

        # Convertir le frame en niveaux de gris pour la détection de visage
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter les visages dans le frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Dessiner un rectangle autour des visages détectés et capturer l'image du visage
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_color = frame[y:y+h, x:x+w]
            image_count += 1
            cv2.imwrite(f"{groupe_directory}/visage_{image_count}.png", roi_color)

        # Afficher le frame avec les visages détectés
        cv2.imshow('Webcam avec capture de visage', frame)

        # Attendre une touche et vérifier si la touche 'q' est pressée pour quitter ce groupe
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Attendre 0.5 seconde entre chaque capture pour réduire la fréquence des captures
        time.sleep(0.5)

    # Passer au groupe suivant
    groupe_count += 1

# Libérer la webcam et détruire toutes les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()
