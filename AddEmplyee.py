import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import sqlite3

class AddEmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un Employé")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.first_name_entry = QLineEdit()
        self.first_name_entry.setPlaceholderText("Prénom")
        layout.addWidget(self.first_name_entry)

        self.last_name_entry = QLineEdit()
        self.last_name_entry.setPlaceholderText("Nom")
        layout.addWidget(self.last_name_entry)

        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText("Adresse")
        layout.addWidget(self.address_entry)

        self.phone_number_entry = QLineEdit()
        self.phone_number_entry.setPlaceholderText("Numéro de téléphone")
        layout.addWidget(self.phone_number_entry)

        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("E-mail")
        layout.addWidget(self.email_entry)

        self.department_id_entry = QComboBox()
        self.department_id_entry.addItem("Sélectionnez le département")
        self.department_id_entry.addItems(["Département 1", "Département 2", "Département 3"])
        layout.addWidget(self.department_id_entry)
        
        self.position_id_entry = QComboBox()
        self.position_id_entry.addItem("Sélectionnez le poste")
        self.position_id_entry.addItems(["Manager", "Employee"])
        layout.addWidget(self.position_id_entry)
        
        self.capture_button = QPushButton("Capturer Visages")
        self.capture_button.clicked.connect(self.capture_faces)
        layout.addWidget(self.capture_button)

        self.add_button = QPushButton("Ajouter Employé")
        self.add_button.clicked.connect(self.add_employee)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        # Couleurs de fond et de texte
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Couleur de fond
        palette.setColor(QPalette.WindowText, Qt.black)  # Couleur de texte
        self.setPalette(palette)

    def add_employee(self):
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        address = self.address_entry.text()
        phone_number = self.phone_number_entry.text()
        email = self.email_entry.text()
        department_id_index = self.department_id_entry.currentIndex()
        position_id_index = self.position_id_entry.currentIndex()

        # Vérifier si tous les champs sont remplis
        if not (first_name and last_name and address and phone_number and email and department_id_index != 0 and position_id_index != 0):
            print("Veuillez remplir tous les champs.")
            return

        # Convertir les index des combobox en entiers
        department_id = department_id_index
        position_id = position_id_index

        # Ajouter l'employé à la base de données
        conn = sqlite3.connect('gestion_employes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Employees (FirstName, LastName, Address, PhoneNumber, Email, DepartmentID, PositionID)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, address, phone_number, email, department_id, position_id))
        conn.commit()
        conn.close()

        print("Employé ajouté avec succès.")

        # Effacer les champs après l'ajout
        self.clear_fields()

    def capture_faces(self):
        print("Fonctionnalité de capture de visages non implémentée.")

    def clear_fields(self):
        self.first_name_entry.clear()
        self.last_name_entry.clear()
        self.address_entry.clear()
        self.phone_number_entry.clear()
        self.email_entry.clear()
        self.department_id_entry.setCurrentIndex(0)
        self.position_id_entry.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = AddEmployeeWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
