import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from Registration import RegistrationPage
from employliste import ViewEmployeesWindow

class LoginRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Login/Register")
        self.setGeometry(700, 400, 300, 200)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h1>Login/Register</h1>")
        layout.addWidget(title_label)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Login and Register buttons
        button_layout = QVBoxLayout()
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        layout.addLayout(button_layout)
        
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)
        
        self.setLayout(layout)

        # Create SQLite database connection
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cursor = self.conn.cursor()

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        try:
            # Query the database to check if the email and password match
            self.cursor.execute("SELECT * FROM Managers WHERE Email=? AND Password=?", (email, password))
            user = self.cursor.fetchone()
            if user:
                self.win = ViewEmployeesWindow()
                self.win.show()
                self.close()
            else:
                QMessageBox.warning(self, "Login Error", "Incorrect email or password. Please try again.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Login Error", "Error occurred during login: " + str(e))

    def register(self):
        self.win = RegistrationPage()
        self.win.show()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterWindow()
    window.show()
    sys.exit(app.exec_())
