import mysql.connector as sql

CURSOR = None
connect = None

STUDENTS_DATABASE = "students_login_data"
TEACHERS_DATABASE = "teachers_login_data"

def init():
    global CURSOR, connect
    connect = sql.connect(host="localhost", user="root", passwd="meradav@2007")
    if connect.is_connected() == False:
        print("Error connecting to mysql")
    CURSOR = connect.cursor(buffered=True)

    try:
        CURSOR.execute("use programming_quiz")
    except:
        # database doesn't exist
        CURSOR.execute("create database programming_quiz")
        CURSOR.execute("use programming_quiz")
    
    try:
        CURSOR.execute(f"select * from {TEACHERS_DATABASE}")
    except:
        #tables don't exist
        CURSOR.execute(f"""create table {TEACHERS_DATABASE}(
                       MENTOR_NAME varchar(100) NOT NULL PRIMARY KEY,
                       PASSWD    varchar(20) NOT NULL)""")
        
    try:
        CURSOR.execute(f"select * from {STUDENTS_DATABASE}")
    except:
        # table doesn't exist
        CURSOR.execute(f"""create table {STUDENTS_DATABASE}(
                       USER_NAME   varchar(100) NOT NULL PRIMARY KEY,
                       PASSWD      varchar(20) NOT NULL,
                       MENTOR_NAME varchar(100) NOT NULL REFERENCES teachers_login_data(MENTOR_NAME)
                       )""")
        
    return CURSOR, connect

init()

def close():
    connect.close()
