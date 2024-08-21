import mysql.connector as sql
import json

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

def update_admins():
    with open("admins.json", 'wt') as f:
        try:
            cursor.execute("select * from programming_quiz_admin_login")
            data = cursor.fetchall()
            
            admins = []
            for i in data:
                admins.append({"Username" : i[0], "Password" : i[1]})
            
            f.seek(0)
            json.dump(admins, f, indent=4)
            f.truncate()
        except:
            pass

update_admins()
