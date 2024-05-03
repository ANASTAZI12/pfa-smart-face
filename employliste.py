import sys
import string
import random
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QDialog,QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class EditEmployeeDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier Employé")
        self.employee_data = employee_data
        self.initUI()
        self.setGeometry(720, 260, 400, 200)

    def initUI(self):
        layout = QVBoxLayout()

        self.name_entry = QLineEdit()
        self.name_entry.setText(self.employee_data[2])
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.name_entry)

        self.lname_entry = QLineEdit()
        self.lname_entry.setText(self.employee_data[3])
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lname_entry)

        self.age_entry = QLineEdit()
        self.age_entry.setText(str(self.employee_data[4]))
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_entry)
        self.age_entry = QLineEdit()

        self.poste_entry = QLineEdit()
        self.poste_entry.setText(str(self.employee_data[6]))
        layout.addWidget(QLabel("Poste:"))
        layout.addWidget(self.poste_entry)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_employee)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_employee(self):
        new_name = self.name_entry.text()
        new_lname = self.lname_entry.text()
        new_age = self.age_entry.text()
        new_poste = self.poste_entry.text()

        try:
            # Modifier les données dans la base de données
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Employees SET FirstName=?, LastName=?, Age=?, PositionID=? WHERE ID=?",
                           (new_name, new_lname, new_age, new_poste, self.employee_data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Employee information updated successfully.")
            self.accept()  # Close the dialog after showing the success message
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")

class ViewEmployeesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Employés")
        self.setGeometry(450, 150, 1000, 800)

        self.initUI()
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cur = self.conn.cursor()
        self.populate_employee_table()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(9)  # ID, Prénom, Nom, Adresse, Téléphone, E-mail, Modifier, Supprimer
        self.employee_table.setHorizontalHeaderLabels(["ID", "Code", "Firs Name", "Last Name", "Age", "Daprtement", "Poste"])

        layout.addWidget(self.employee_table)

        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee_dialog)
        layout.addWidget(self.add_employee_button)

        self.central_widget.setLayout(layout)

    def populate_employee_table(self):
        self.cur.execute("SELECT * FROM Employees")
        employees = self.cur.fetchall()
        if employees:
            self.employee_table.setRowCount(len(employees))
            for row, employee in enumerate(employees):
                for col, data in enumerate(employee):
                    item = QTableWidgetItem(str(data))
                    self.employee_table.setItem(row, col, item)

                # Ajouter les boutons Modifier et Supprimer
                edit_button = QPushButton("Modifier")
                edit_button.clicked.connect(lambda _, row=row: self.edit_employee(row))
                self.employee_table.setCellWidget(row, 7, edit_button)

                delete_button = QPushButton("Supprimer")
                delete_button.clicked.connect(lambda _, row=row: self.delete_employee(row))
                self.employee_table.setCellWidget(row, 8, delete_button)
        else:
            self.employee_table.setRowCount(1)
            item = QTableWidgetItem("Aucun employé trouvé")
            item.setTextAlignment(Qt.AlignCenter)
            self.employee_table.setItem(0, 0, item)

    def edit_employee(self, row):
        # Récupérer les données de l'employé sélectionné
        employee_id = int(self.employee_table.item(row, 0).text())
        self.cur.execute("SELECT * FROM Employees WHERE ID=?", (employee_id,))
        employee_data = self.cur.fetchone()
        dialog = EditEmployeeDialog(employee_data, parent=self)
        if dialog.exec_():
            self.populate_employee_table()

    def delete_employee(self, row):
        # Récupérer l'ID de l'employé sélectionné
        employee_id = int(self.employee_table.item(row, 0).text())
        # Supprimer l'employé de la base de données
        self.cur.execute("DELETE FROM Employees WHERE ID=?", (employee_id,))
        self.conn.commit()
        self.populate_employee_table()

    def add_employee_dialog(self):
        dialog = AddEmployeeDialog(parent=self)
        if dialog.exec_():
            self.populate_employee_table()


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter Employé")
        self.initUI()
        self.setGeometry(720, 260, 400, 200)

    def initUI(self):
        layout = QVBoxLayout()

        self.name_entry = QLineEdit()
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.name_entry)

        self.lname_entry = QLineEdit()
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lname_entry)

        self.age_entry = QLineEdit()  # Corrected variable name
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_entry)  # Corrected variable name

        self.poste_entry = QLineEdit()  # Corrected variable name
        layout.addWidget(QLabel("Poste:"))
        layout.addWidget(self.poste_entry)  # Corrected variable name

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 250)

        self.add_image_button = QPushButton("Add Image")
        self.add_image_button.clicked.connect(self.select_image)

        layout.addWidget(QLabel("Image:"))
        layout.addWidget(self.image_label)
        layout.addWidget(self.add_image_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_employee)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)", options=options)
        if file_path:
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaledToWidth(200)  # Scale the pixmap to fit within QLabel
            self.image_label.setPixmap(pixmap)

    def save_employee(self):
        name = self.name_entry.text()
        lname = self.lname_entry.text()
        age = self.age_entry.text()
        poste = self.poste_entry.text()
        emp_code = generate_random_code()

        if name == "" or lname == "" or age == "" or poste == "":
            QMessageBox.warning(self, "Registration Error", "All fields must be filled out")
        else:
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()
            # Read image data as bytes
            image_data = None
            if self.image_label.pixmap():  # Check if pixmap is set
                pixmap = self.image_label.pixmap()
                pixmap.save("temp_image.jpg", quality=100)  # Save pixmap to temporary file
                with open("temp_image.jpg", "rb") as file:
                    image_data = file.read()  # Read image data from file

            try:
                cursor.execute("INSERT INTO Employees(Code, FirstName, LastName, Age, DepartmentID, PositionID, Image) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (emp_code, name, lname, age, 1, poste, image_data))
                conn.commit()

                if cursor.rowcount > 0:
                    QMessageBox.information(self, "Success", "Employee added successfully.")
                    self.accept()  # Close the dialog only if the employee is added successfully
                else:
                    QMessageBox.warning(self, "Error", "Failed to add employee.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {e}")

            conn.close()


def main():
    app = QApplication(sys.argv)
    window = ViewEmployeesWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
