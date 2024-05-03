import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit,QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3 

class ViewEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Employee")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.info_layout = QVBoxLayout()  # Layout to hold employee information
        layout.addLayout(self.info_layout)

        self.code_entry = QLineEdit()
        self.code_entry.setPlaceholderText("Enter Employee Code")
        layout.addWidget(self.code_entry)

        self.display_button = QPushButton("Display Employee")
        self.display_button.clicked.connect(self.display_employee)
        layout.addWidget(self.display_button)

        self.setLayout(layout)

    def display_employee(self):
        code = self.code_entry.text()
        if code:
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Employees WHERE Code=?", (code,))
            employee_data = cursor.fetchone()

            if employee_data:
                # Clear existing labels from the layout
                for i in reversed(range(self.info_layout.count())):
                    self.info_layout.itemAt(i).widget().deleteLater()

                # Display employee information
                info_labels = [
                    f"First Name: {employee_data[1]}",
                    f"Last Name: {employee_data[2]}",
                    f"Age: {employee_data[3]}",
                    f"Poste: {employee_data[4]}"
                    # Add more fields as needed
                ]
                for info in info_labels:
                    label = QLabel(info)
                    self.info_layout.addWidget(label)

                # Display employee image if available
                image_data = employee_data[6]  # Assuming image data is stored in the 7th column
                if image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    self.image_label.setPixmap(pixmap.scaledToWidth(200))  # Adjust width as needed
                else:
                    self.image_label.clear()
            else:
                QMessageBox.warning(self, "Employee Not Found", "Employee with the provided code was not found.")
            
            conn.close()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a code.")
