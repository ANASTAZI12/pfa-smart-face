import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QColor

class RegistrationPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration Page")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("<h1 style='color: #333;'>Registration</h1>")
        layout.addWidget(title_label)

        # Champs d'insertion de données
        self.first_name_entry = QLineEdit()
        self.first_name_entry.setPlaceholderText("Enter First Name")
        self.first_name_entry.setStyleSheet("background-color: #eee; color: #333;")
        layout.addWidget(self.first_name_entry)

        self.last_name_entry = QLineEdit()
        self.last_name_entry.setPlaceholderText("Enter Last Name")
        self.last_name_entry.setStyleSheet("background-color: #eee; color: #333;")
        layout.addWidget(self.last_name_entry)

        self.age_entry = QLineEdit()
        self.age_entry.setPlaceholderText("Enter Age")
        self.age_entry.setStyleSheet("background-color: #eee; color: #333;")
        layout.addWidget(self.age_entry)

        self.poste_entry = QLineEdit()
        self.poste_entry.setPlaceholderText("Enter Poste")
        self.poste_entry.setStyleSheet("background-color: #eee; color: #333;")
        layout.addWidget(self.poste_entry)

        # Bouton d'enregistrement
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.register_button.clicked.connect(self.register_employee)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_employee(self):
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        age = self.age_entry.text()
        poste = self.poste_entry.text()

        # Vérifier si tous les champs sont remplis
        if not (first_name and last_name and age and poste):
            QMessageBox.warning(self, "Missing Information", "Please fill all fields.")
            return

        try:
            age = int(age)  # Convertir l'âge en entier
        except ValueError:
            QMessageBox.warning(self, "Invalid Age", "Age must be a number.")
            return

        # Insérer l'employé dans la base de données (à compléter)

        QMessageBox.information(self, "Registration Successful", "Employee registered successfully.")

        # Effacer les champs après l'inscription
        self.clear_fields()

    def clear_fields(self):
        self.first_name_entry.clear()
        self.last_name_entry.clear()
        self.age_entry.clear()
        self.poste_entry.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    registration_page = RegistrationPage()
    registration_page.show()
    sys.exit(app.exec_())
