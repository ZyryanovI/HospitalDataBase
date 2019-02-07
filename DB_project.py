import sqlite3

conn = sqlite3.connect("my_bd.db")

cur = conn.cursor()

cur.execute('''
   CREATE TABLE Patients (
       id INTEGER PRIMARY KEY,
       phone_number VARCHAR(255),
       name VARCHAR(255),
       surname VARCHAR(255),
       patronymic VARCHAR(255),
       gender CHAR,
       date_of_birth VARCHAR(255),
       adress VARCHAR(255)
   )
''')

cur.execute('''
    CREATE TABLE For_Stationary(
        id_patient INTEGER,
        ward INTEGER,
        diet VARCHAR(255),
        arival_date VARCHAR(10),
        leaving_date VARCHAR(10),
        FOREIGN KEY(id_patient) REFERENCES Patients(id)
    )
''')

cur.execute('''
    CREATE TABLE Doctors_Personal_Info(
        id INTEGER PRIMARY KEY,
        phone_number VARCHAR(255),
        name VARCHAR(255),
        surname VARCHAR(255),
        patronymic VARCHAR(255),
        salary INTEGER,
        begin_of_contract VARCHAR(10),
        end_of_contract VARCHAR(10)
    )
''')

cur.execute('''
    CREATE TABLE Inspection(
        id INTEGER PRIMARY KEY,
        id_patient INTEGER,
        id_doc INTEGER,
        result VARCHAR(255),
        start_time VARCHAR(16),
        ending_time VARCHAR(16),
        FOREIGN KEY(id_patient) REFERENCES Patients(id),
        FOREIGN KEY(id_doc) REFERENCES Doctors_Personal_Info(id)
    )
''')

cur.execute('''
    CREATE TABLE Sponsors(
        id INTEGER PRIMARY KEY,
        phone_number VARCHAR(255),
        name VARCHAR(255)
    )
''')

cur.execute('''
    CREATE TABLE Payment(
        id INTEGER PRIMARY KEY,
        id_sponsor INTEGER,
        amount INTEGER,
        date VARCHAR(10),
        FOREIGN KEY(id_sponsor) REFERENCES Sponsors(id)
    )
''')

cur.execute('''
    CREATE Table Target_Payment(
        id INTEGER PRIMARY KEY,
        reason VARCHAR(255),
        date VARCHAR(10),
        amount INTEGER
    )
''')

cur.execute('''
    CREATE TABLE Personal_Payment(
        id INTEGER PRIMARY KEY,
        recipient_id INTEGER,
        reason VARCHAR(255),
        date VARCHAR(10),
        amount INTEGER,
        FOREIGN KEY(recipient_id) REFERENCES Doctors_Personal_Info(id)
    )
''')

cur.execute('''
    CREATE TABLE Payment_Communication(
        id_payment INTEGER,
        id_payment_hospital INTEGER,
        FOREIGN KEY(id_payment) REFERENCES Payment(id),
        FOREIGN KEY(id_payment_hospital) REFERENCES Personal_Payment(id)
    )
''')

cur.execute('''
    CREATE TABLE Procedure(
        id INTEGER PRIMARY KEY,
        id_patient INTEGER,
        type VARCHAR(255),
        start VARCHAR(255),
        finish VARCHAR(255),
        done BOOLEAN,
        FOREIGN KEY(id_patient) REFERENCES Patients(id)
    )
''')

cur.execute('''
    CREATE TABLE Doctors_and_Procedure(
        id_doctor INTEGER,
        id_procedure INTEGER,
        FOREIGN KEY(id_doctor) REFERENCES Doctors_Personal_Info(id),
        FOREIGN KEY(id_procedure) REFERENCES Procedure(id)
    )
''')

cur.execute('''
    CREATE TABLE Specialty_And_Doc(
        id_doc INTEGER,
        spec_name VARCHAR(255),
        FOREIGN KEY(id_doc) REFERENCES Doctors_Personal_Info(id)
    )
''')

cur.execute('''
    CREATE TABLE Analyzes(
        id INTEGER PRIMARY KEY,
        id_patient INTEGER,
        type VARCHAR(255),
        start_time VARCHAR(10),
        short_res VARCHAR(255),
        result VARCHAR(255),
        FOREIGN KEY(id_patient) REFERENCES Patient(id)
    )
''')

cur.execute('''
    CREATE TABLE Docs_And_Analyzes(
        id_doc INTEGER,
        id_analyz INTEGER,
        FOREIGN KEY(id_doc) REFERENCES Doctors_Personal_Info(id),
        FOREIGN KEY(id_analyz) REFERENCES Analyzes(id)
    )
''')

cur.execute('''
    CREATE TABLE Disease_History(
        id INTEGER PRIMARY KEY,
        id_patient INTEGER,
        diagnosis VARCHAR(255),
        start_treatment VARCHAR(10),
        end_treatment VARCHAR(10),
        FOREIGN KEY(id_patient) REFERENCES Patient(id)
    )
''')

cur.execute('''
    CREATE TABLE Doctors_and_Disease(
        id_doctor INTEGER,
        id_disease INTEGER,
        FOREIGN KEY(id_doctor) REFERENCES Doctors_Personal_Info(id),
        FOREIGN KEY(id_disease) REFERENCES Disease_History(id)
    )
''')

cur.execute('''
    CREATE TABLE Notation(
        id_disease INTEGER,
        date VARCHAR(10),
        notation VARCHAR(255),
        FOREIGN KEY(id_disease) REFERENCES Disease_History(id)
    )
''')

conn.commit()

conn.close()
