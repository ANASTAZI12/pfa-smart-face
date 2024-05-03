import cv2

# Créer un objet VideoCapture pour accéder à la webcam
cap = cv2.VideoCapture(0)  # 0 pour la webcam par défaut

# Charger le détecteur de visage Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Noms des personnes à reconnaître (correspondent à l'ordre des visages détectés)
noms = ["anas", "Personne 2", "Personne 3"]

# Vérifier si la webcam est ouverte correctement
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

# Lire les images de la webcam en continu
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
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Dessiner un rectangle autour des visages détectés et afficher le nom
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, noms[i], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Afficher le frame avec les visages détectés et les noms
    cv2.imshow('Webcam avec détection de visage et noms', frame)

    # Attendre une touche et vérifier si la touche 'q' est pressée pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et détruire toutes les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()
