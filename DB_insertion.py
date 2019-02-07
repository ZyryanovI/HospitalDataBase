import sqlite3
import random


def check_month_or_d(x):
    if x < 10:
        return "0" + str(x)
    else:
        return str(x)


The_Most_Important_ID = 0

conn = sqlite3.connect("my_bd.db")

cur = conn.cursor()

names_ = ["Петр", "Андрей", "Федор", "Афанасий", "Евгений", "Иван"]

surnames_ = ["Петров", "Сидоров", "Букреев", "Субботин", "Якунин"]

patronymics_ = ["Петрович", "Андреевич", "Федорович", "Афанасьевич", "Евгеньевич", "Иванович"]

phone_numbers_ = [str(80000000000 + i) for i in range(400)]

adresses_ = ["Улица {} дом {}".format(random.randint(1, 100),
                                      random.randint(1, 100)) for i in range(200)]

dates_start = []
dates_end = []
for i in range(300):
    year = random.randint(1950, 2018)
    month = random.randint(0, 12)
    date = random.randint(1, 30)

    dates_start.append("{}:{}:{}".format(year, check_month_or_d(month),
                                         check_month_or_d(date)))

    year_end = year + random.randint(0, 1)
    month_end = (month + random.randint(0, 12)) % 13
    date_end = (date + random.randint(0, 31)) % 31

    dates_end.append("{}:{}:{}".format(year_end, check_month_or_d(month),
                                       check_month_or_d(date)))


time_start = []
time_end = []
for i in range(300):
    year = random.randint(1950, 2018)
    month = random.randint(0, 12)
    date = random.randint(1, 30)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    time_start.append("{}:{}:{}:{}:{}".format(year,
                                               check_month_or_d(month),
                                               check_month_or_d(date),
                                               check_month_or_d(hour),
                                               check_month_or_d(minute)))

    year_end = year + random.randint(0, 1)
    month_end = (month + random.randint(0, 12)) % 13
    date_end = (date + random.randint(0, 31)) % 31
    hour_end = (hour + random.randint(0, 23)) % 24
    minute_end = (minute + random.randint(0, 59)) % 60

    time_end.append("{}:{}:{}:{}:{}".format(year_end,
                                             check_month_or_d(month_end),
                                             check_month_or_d(date_end),
                                             check_month_or_d(hour_end),
                                             check_month_or_d(minute_end)))


dietes_ = ["Морковь", "Суп", "Фуагра"]

specialties_ = ["Хирург", "Терапевт", "Стоматолог", "Кардиолог", "Невролог"]

procedurses_ = ["массаж", "лимфодринаж", "электрофорез", "ЛФК"]

analyzes_types = ["Анализ на гемоглобин", "СОЭ", "Анализ крови на сахар", "ПЦР"]

diagnosis = ["ОРВ", "Грипп", "Перелом", "Язва", "Анемия"]

sponsors_names = ["Зырянов Илья Евгеньевич", "МФТИ", "Министерство зравоохранения Камбоджи"]

for i in range(97):
    sponsors_names.append("Добрый спонсор {}".format(i))


target_reasons_ = ["Закупка рентгеновского аппарата", "Починка крыльца больницы",
                   "Закупка аппаратуры для анализов"]

personal_reason_ = ["Премия", "Зарплата"]

MAX_DATE = "2100:01:01"
MAX_TIME = "2100:01:01:01:01"

#  ************************************************************************************

# пациенты 0-99

for i in range(100):
    cur.execute('''INSERT INTO Patients (id, phone_number, name, surname, patronymic,
     gender, date_of_birth, adress) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                                                         random.choice(phone_numbers_),
                                                        random.choice(names_),
                                                        random.choice(surnames_),
                                                        random.choice(patronymics_),
                                                        random.choice(["M", "F"]),
                                                        random.choice(dates_start),
                                                        random.choice(adresses_)))
    The_Most_Important_ID += 1

#  стационар

for i in range(75):
    cur.execute('''INSERT INTO For_Stationary 
    (id_patient, ward, diet, arival_date, leaving_date) VALUES (?, ?, ?, ?, ?)''',
                (i, i, random.choice(dietes_), random.choice(dates_start), random.choice(dates_end)))

for i in range(25):
    cur.execute('''INSERT INTO For_Stationary 
    (id_patient, ward, diet, arival_date, leaving_date) VALUES (?, ?, ?, ?, ?)''',
                (i, i, random.choice(dietes_), random.choice(dates_start), MAX_DATE))

#  доктора 100-199

for i in range(100):
    cur.execute('''INSERT INTO Doctors_Personal_Info (id, phone_number, name, surname, 
    patronymic, salary, begin_of_contract, end_of_contract) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (The_Most_Important_ID,
                 random.choice(phone_numbers_),
                 random.choice(names_),
                 random.choice(surnames_),
                 random.choice(patronymics_),
                 random.randint(15000, 50000),
                 random.choice(dates_start),
                 random.choice(dates_end)))
    The_Most_Important_ID += 1

# осмотры 200-299s

for i in range(100):
    cur.execute('''INSERT INTO Inspection (id, id_patient, id_doc,
     result, start_time, ending_time) 
     VALUES (?, ?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                   random.randint(0, 99),
                                   random.randint(100, 199),
                                   random.choice(["healthy", "ill", "quite ok"]),
                                   random.choice(time_start),
                                   random.choice(time_end)))
    The_Most_Important_ID += 1

#  специальности докторов
doc_counter = 100
for i in range(100):
    cur.execute('''INSERT INTO Specialty_And_Doc (id_doc, spec_name)
    VALUES (?, ?)''', (doc_counter, random.choice(specialties_)))
    doc_counter += 1


#  процедуры 300-399

for i in range(100):
    cur.execute('''INSERT INTO Procedure (id, id_patient, type, start, finish, done)
    VALUES (?, ?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                  random.randint(0, 99),
                                  random.choice(procedurses_),
                                  random.choice(time_start),
                                  random.choice(time_end),
                                  random.choice([True, False])))
    The_Most_Important_ID += 1


for i in range(100):
    cur.execute('''INSERT INTO DOCTORS_and_Procedure (id_doctor, id_procedure)
    VALUES (?, ?)''', (random.randint(100, 199),
                       random.randint(300, 399)))


#  анализы 400-499

for i in range(100):
    cur.execute('''INSERT INTO Analyzes (id, id_patient, type, 
    start_time, short_res, result) VALUES (?, ?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                                                 random.randint(0, 99),
                                                                 random.choice(analyzes_types),
                                                                 random.choice(time_start),
                                                                 random.choice(["OK", "NOT OK"]),
                                                                 "Здесь какой-то очень важный текст"))
    The_Most_Important_ID += 1


for i in range(100):
    cur.execute('''INSERT INTO Docs_And_Analyzes (id_doc, id_analyz) VALUES
    (?, ?)''', (random.randint(100, 199), random.randint(400, 499)))


#  История болезни 500-599

for i in range(70):
    cur.execute('''INSERT INTO Disease_History (id, id_patient, diagnosis,
     start_treatment, end_treatment) VALUES (?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                                                random.randint(0, 99),
                                                                random.choice(diagnosis),
                                                                random.choice(dates_start),
                                                                random.choice(dates_end)))
    The_Most_Important_ID += 1

for i in range(30):
    cur.execute('''INSERT INTO Disease_History (id, id_patient, diagnosis,
     start_treatment, end_treatment) VALUES (?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                                                                random.randint(0, 99),
                                                                random.choice(diagnosis),
                                                                random.choice(dates_start),
                                                                MAX_DATE))
    The_Most_Important_ID += 1


for i in range(100):
    cur.execute('''INSERT INTO Doctors_and_Disease (id_doctor, id_disease)
    VALUES (?, ?)''', (random.randint(100, 199), random.randint(500, 599)))

for i in range(300):
    cur.execute('''INSERT INTO Notation (id_disease, date, notation)
    VALUES (?, ?, ?)''', (random.randint(500, 599),
                         random.choice(dates_start),
                         "Какой-то очень важный текст"))


#  спонсоры 600-699

for i in range(100):
    cur.execute("INSERT INTO Sponsors (id, phone_number, name) VALUES (?, ?, ?)",
                (The_Most_Important_ID, random.choice(phone_numbers_),
                 random.choice(sponsors_names)))
    The_Most_Important_ID += 1


#  выплаты 700-799
for i in range(100):
    cur.execute('''INSERT INTO Payment (id, id_sponsor, amount, date) VALUES
    (?, ?, ?, ?)''', (The_Most_Important_ID, random.randint(600, 699),
                      random.randint(100000, 5000000), random.choice(dates_start)))
    The_Most_Important_ID += 1

#  целевые выплаты 800-899
for i in range(100):
    cur.execute('''INSERT INTO Target_Payment (id, reason, date, amount)
    VALUES (?, ?, ?, ?)''', (The_Most_Important_ID, random.choice(target_reasons_),
                            random.choice(dates_start), random.randint(1000000, 2000000)))
    The_Most_Important_ID += 1

#  персональные выплаты 900-999
for i in range(100):
    cur.execute('''INSERT INTO Personal_Payment (id, recipient_id, reason, date, amount)
    VALUES (?, ?, ?, ?, ?)''', (The_Most_Important_ID,
                               random.randint(100, 199),
                               random.choice(personal_reason_),
                               random.choice(dates_start),
                               random.randint(5000, 50000)))
    The_Most_Important_ID += 1


for i in range(100):
    cur.execute('''INSERT INTO Payment_Communication (id_payment,
     id_payment_hospital) VALUES (?, ?)''', (random.randint(700, 799),
                                             random.randint(800, 999)))


conn.commit()

conn.close()
