import sqlite3

# Connexion à la base de données SQLite (crée un fichier de base de données s'il n'existe pas)
conn = sqlite3.connect('gestion_des_employes.db')
cursor = conn.cursor()

# Création de la table des Employés
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code VARCHAR(30),
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    Age INTEGER,
    DepartmentID INTEGER,
    PositionID VARCHAR(30),
    Image BLOB,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);
''')
# Création de la table des Horaires de Travail
cursor.execute('''
CREATE TABLE IF NOT EXISTS WorkSchedule (
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID INTEGER,
    WorkDate DATE,
    StartTime TIME,
    EndTime TIME,
    DayOff INTEGER,
    OvertimeHours DECIMAL(5, 2),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);
''')

# Création de la table des Départements
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    DepartmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartmentName VARCHAR(30),
    Description VARCHAR(30),
    DepartmentHead INTEGER,
    FOREIGN KEY (DepartmentHead) REFERENCES Employees(EmployeeID)
);
''')

# Création de la table des Postes
cursor.execute('''
CREATE TABLE IF NOT EXISTS Positions (
    PositionID INTEGER PRIMARY KEY AUTOINCREMENT,
    PositionName VARCHAR(30),
    Description VARCHAR(30),
    SalaryLevel DECIMAL(10, 2)
);
''')

# Création de la table des Performances
cursor.execute('''
CREATE TABLE IF NOT EXISTS Performances (
    PerformanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID INTEGER,
    EvaluationDate DATE,
    PerformanceRating INTEGER,
    AchievedGoals VARCHAR(30),
    Rewards VARCHAR(30),
    Penalties VARCHAR(30),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);
''')

# Création de la table des Gestionnaires
cursor.execute('''
CREATE TABLE IF NOT EXISTS Managers (
    ManagerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    DepartmentID INTEGER,
    Email VARCHAR(30),
    Password VARCHAR(30),
    Role VARCHAR(30)
);
''')
# Valider les modifications et fermer la connexion
conn.commit()
conn.close()
