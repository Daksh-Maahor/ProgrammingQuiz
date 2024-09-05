import mysql.connector as sql
import json
import traceback

connect = sql.connect(host="localhost", user="root", passwd="meradav@2007")

if connect.is_connected():
    print("connected")

cursor = connect.cursor()

cursor.execute("create database if not exists programming_quiz")
cursor.execute("use programming_quiz")

try:
    cursor.execute("create table programming_quiz_admin_login(user_id varchar(50) not null primary key, user_password varchar(50) not null)")
except:
    pass

try:
    cursor.execute("create table programming_quiz_student_login(user_id varchar(50) not null primary key, user_password varchar(50) not null)")
except:
    pass

def update_admins_and_students():
    file_data = []
    with open("admins.json", "rt") as f:
        try:
            file_data = json.load(f)
            print(file_data)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    with open("admins.json", 'wt') as f:
        try:
            cursor.execute("select * from programming_quiz_admin_login")
            sql_data = cursor.fetchall()
            
            user_names = []
            admins = []
            for i in file_data:
                if not i['Username'] in user_names:
                    admins.append({"Username" : i['Username'], "Password" : i['Password']})
                    user_names.append(i['Username'])
            
            for i in sql_data:
                if not i[0] in user_names:
                    admins.append({"Username" : i[0], "Password" : i[1]})
                    user_names.append(i[0])
            
            f.seek(0)
            json.dump(admins, f, indent=4)
            f.truncate()
            
            cursor.execute("truncate programming_quiz_admin_login")
            connect.commit()
            
            for i in admins:
                cursor.execute(f'insert into programming_quiz_admin_login values("{i['Username']}", "{i['Password']}")')
                connect.commit()
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    file_data = []
    with open("students.json", "rt") as f:
        try:
            file_data = json.load(f)
            print(file_data)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    with open("students.json", 'wt') as f:
        try:
            cursor.execute("select * from programming_quiz_student_login")
            sql_data = cursor.fetchall()
            
            user_names = []
            students = []
            for i in file_data:
                if not i['Username'] in user_names:
                    students.append({"Username" : i['Username'], "Password" : i['Password']})
                    user_names.append(i['Username'])
            
            for i in sql_data:
                if not i[0] in user_names:
                    students.append({"Username" : i[0], "Password" : i[1]})
                    user_names.append(i[0])
            
            f.seek(0)
            json.dump(students, f, indent=4)
            f.truncate()
            
            cursor.execute("truncate programming_quiz_student_login")
            connect.commit()
            
            for i in students:
                cursor.execute(f'insert into programming_quiz_student_login values("{i['Username']}", "{i['Password']}")')
                connect.commit()
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    

update_admins_and_students()
