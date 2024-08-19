import mysql.connector as sql

connect = sql.connect(host="localhost", user="root", passwd="meradav@2007")

if connect.is_connected():
    print("connected")

cursor = connect.cursor()

cursor.execute("create database if not exists programming_quiz")
cursor.execute("use programming_quiz")

cursor.execute("drop table if exists programming_quiz_admin_login")
cursor.execute("create table programming_quiz_admin_login(user_id varchar(30) not null primary key, user_password varchar(20) not null)")
