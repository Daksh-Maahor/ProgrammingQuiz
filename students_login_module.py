import json
import mysql
import mysql.connector
import __init__ as sql


def login() -> tuple[str, str]:  # returns (username, password). None in both if login fails.
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    sql.cursor.execute(f'select user_id, user_password from programming_quiz_student_login where user_id = "{user_name}"')
    
    data = sql.cursor.fetchall()
    
    if len(data) == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
    else:
        data = data[0]
        if pass_key != data[1]:
            print("Invalid Password")
            print()
            print()
        else:
            print("Login Successful")
            print(f"Welcome {user_name}")
            print()
            print()
            
            return user_name, pass_key
    
    return None, None

def sign_up(): # returns Nothing. as registration does not confirm login
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    sql.cursor.execute(f'select user_id, user_password from programming_quiz_student_login where user_id = "{user_name}"')
    
    data = sql.cursor.fetchall()
    
    if len(data) == 0:
        sql.cursor.execute(f'insert into programming_quiz_student_login values("{user_name}", "{pass_key}")')
        sql.connect.commit()
        print("Registration Successful.")
        sql.update_admins_and_students()
        print()
        print()
    else:
        print(f"User ID {user_name} already exists.")
        print()
        print()
        return
    
def update_passkey() -> str: # returns password, as that's what has changed
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    sql.cursor.execute(f'select user_id, user_password from programming_quiz_student_login where user_id = "{user_name}"')
    
    data = sql.cursor.fetchall()
    
    if len(data) == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
        return pass_key
    else:
        data = data[0]
        if pass_key != data[1]:
            print("Invalid Password")
            print()
            print()
            return pass_key
        else:
            print("Enter new Password : ")
            pass_key = input(">> ")
            
            sql.cursor.execute(f'update programming_quiz_student_login set user_password="{pass_key}" where user_id="{user_name}"')
            sql.connect.commit()
            print("Password Changed Successfully!")
            print()
            print()
            
            return pass_key

