import sqlite3

MAX_DATE = "2100:01:01"
MAX_TIME = "2100:01:01:01:01"

conn = sqlite3.connect("my_bd.db")


def req0():
    cur = conn.cursor()
    cur.execute('''SELECT start_time, ending_time
                   FROM Inspection
                   JOIN (SELECT id
                         FROM Doctors_Personal_Info
                         WHERE (name = "Федор") AND (surname = "Субботин") AND (patronymic = "Андреевич")) AS A 
                   ON A.id = Inspection.id 
                   WHERE start_time > "2018:05:25"''')
    res = cur.fetchall()
    print(res)


'''WHERE '''

# Номера и названия спонсоров, внесших пожертвования после 01.01.2018
def request1():
    cur = conn.cursor()
    cur.execute('''SELECT name, phone_number
                   FROM Sponsors
                   JOIN (SELECT id_sponsor 
                         FROM Payment 
                         WHERE date > "2018:01:01") ON id_sponsor = id''')
    res = cur.fetchall()
    print(res)


# Телефоны, ФИО и дата рождения всех пациентов старше 18
def request2():
    cur = conn.cursor()
    cur.execute('''SELECT phone_number, name, surname, patronymic, date_of_birth
                   FROM Patients
                   WHERE date_of_birth < "2000:05:17"''')
    res = cur.fetchall()
    print(res)


# узнать телефон и ФИО докторов лечащих пациента с id 45
def request3():
    cur = conn.cursor()
    cur.execute('''SELECT phone_number, name, surname, patronymic
                   FROM Doctors_Personal_Info
                   JOIN (SELECT id_doctor
                         FROM Doctors_and_Disease
                         JOIN (SELECT Disease_History.id
                               FROM Disease_History
                               WHERE (id_patient = 45) AND (end_treatment = "2100:01:01")) 
                         ON id_disease = id) 
                   ON id_doctor = id''')
    res = cur.fetchall()
    print(res)


# вывести номер телефона, ФИО и диагноз всех пациентов,
# которые в данный момент лечатся
def request4():
    cur = conn.cursor()
    cur.execute('''SELECT phone_number, name, surname, patronymic, diagnosis
                   FROM Patients
                   JOIN (SELECT id_patient, diagnosis
                         FROM Disease_History
                         WHERE end_treatment = "2100:01:01") ON id_patient = id''')
    res = cur.fetchall()
    print(res)


# узнать информацию о выплатах, сделаных врачу с id 114
def request5():
    cur = conn.cursor()
    cur.execute('''SELECT amount, reason, date, name, surname, patronymic
                   FROM Personal_Payment, Doctors_Personal_Info
                   WHERE (recipient_id = 114) AND (Doctors_Personal_Info.id = 114)''')

    res = cur.fetchall()
    print(res)


# узнать сумму зарплат всех врачей
def request6():
    cur = conn.cursor()
    cur.execute('''SELECT SUM(salary)
                   FROM Doctors_Personal_Info
                   ''')

    res = cur.fetchall()
    print(res)


# узнать телефон, ФИО, номера палат, у пациентов,
#  которые в данный момент лежат в стационаре
def request7():
    cur = conn.cursor()
    cur.execute('''SELECT phone_number, name, surname, patronymic, ward
                   FROM (SELECT *
                         FROM For_Stationary
                         WHERE leaving_date = "2100:01:01")
                   JOIN Patients ON id = id_patient''')

    res = cur.fetchall()
    print(res)


# Узнать, какие типы анализов были приняты врачем с id 156 после 01.02.1997
def request8():
    cur = conn.cursor()
    cur.execute('''SELECT type
                   FROM Analyzes
                   JOIN (SELECT id_analyz
                         FROM Docs_and_Analyzes
                         WHERE id_doc = 156) ON id_analyz = id
                   WHERE start_time > "1997:02:01"''')

    res = cur.fetchall()
    print(res)


# какие целевые выплатыбыли сделаны больницей за 2017 год
def request9():
    cur = conn.cursor()
    cur.execute('''SELECT reason, date, amount
                   FROM Target_Payment
                   WHERE (date >= "2017:01:01") AND (date < "2018:01:01")''')

    res = cur.fetchall()
    print(res)


# еще можно поработать с осмотрами, записями в истории болезни,
# процедурами и мб анализами

# результат осмотров для пациента с id 14
def request10():
    cur = conn.cursor()
    cur.execute('''SELECT result, phone_number, name, surname, patronymic
                   FROM Inspection, Patients
                   WHERE (id_patient = 14) AND (Patients.id = 14)''')

    res = cur.fetchall()
    print(res)


# специальности врачей, у которых контракт заканчивается в 2018
def request11():
    cur = conn.cursor()
    cur.execute('''SELECT spec_name
                   FROM Specialty_And_Doc
                   JOIN (SELECT id
                         FROM Doctors_Personal_Info
                         WHERE (end_of_contract > "2018:00:00") AND (end_of_contract < "2019:00:00")) 
                   ON id = id_doc''')

    res = cur.fetchall()
    print(res)


# записи в историю болезни пациента с id 67, отсортированные по дате
def request12():
    cur = conn.cursor()
    cur.execute('''SELECT date, notation
                   FROM Notation
                   JOIN (SELECT id
                         FROM Disease_History
                         WHERE id_patient = 67) ON id = id_disease
                   ORDER BY date''')

    res = cur.fetchall()
    print(res)


# какие процедурыы прошел пациент с id 46 в 2018 году
def request13():
    cur = conn.cursor()
    cur.execute('''SELECT type, start
                   FROM Procedure
                   WHERE (id_patient = 46) AND (done = 1) AND (start > "2018:00:00")''')

    res = cur.fetchall()
    print(res)


# В sqlite нет оконных функций, поэтому запросы будут тут просто строчкой


# 1) узнать какой спонсор сколько заплатил суммарно
# (оконная функция норм, т.к. быстрее чем подзапросы)
'''SELECT phone_number, name,
          SUM(amount) OVER(PARTITION BY id_sponsor) AS Total
   FROM Sponsors
   JOIN Payment ON id_sponsor = Sponsor.id'''

# 2) Хотим узнать сколько суммарно и сколько по количеству
# было сделано персональных ваплат докторам с разными id
'''SELECT id, SUM(amount) OVER(PARTITION BY id) AS Total,
          COUNT(amount) OVER(PARTITION BY id) AS amount_count
   FROM Personal_Payment'''

# 3) вывести сгруппированные по id истрории болезни(id, диагноз, время начала лечения)
# отсортированные по дате начала, при этом не закончившиеся
'''SELECT id, diagnosis, start_treatment
   FROM Disease_History
   OVER(PARTITION BY id
        ORDER BY start_treatment)
   WHERE end_treatment = "2100:01:01"'''


if __name__ == '__main__':
    req0()
    request1()
    request2()
    request3()
    request4()
    request5()
    request6()
    request7()
    request8()
    request9()
    request10()
    request11()
    request12()
    request13()

    conn.commit()

    conn.close()
