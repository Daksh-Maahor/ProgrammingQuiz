import json
import mysql
import mysql.connector
import __init__ as sql

def login():
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    sql.cursor.execute(f'select user_id, user_password from programming_quiz_admin_login where user_id = "{user_name}"')
    
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
            return
        else:
            print("Login Successful")
            print(f"Welcome {user_name}")
            print()
            print()

def sign_up():
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    sql.cursor.execute(f'select user_id, user_password from programming_quiz_admin_login where user_id = "{user_name}"')
    
    data = sql.cursor.fetchall()
    
    if len(data) == 0:
        sql.cursor.execute(f'insert into programming_quiz_admin_login values("{user_name}", "{pass_key}")')
        sql.connect.commit()
        print("Registration Successful.")
        print()
        print()
    else:
        print(f"User ID {user_name} already exists.")
        print()
        print()
        return

def main():
    print("----   Programming Quiz   ----")
    print("----   Teacher's Module   ----")

    print()
    
    running = True
    
    while running:

        print("Select An Option")
        print("1. Login")
        print("2. Sign Up")
        print("3. Quit")

        choice = input(">> ")
        
        if not choice.isnumeric():
            print("Invalid Choice")
            print()
            continue
        
        choice = int(choice)

        if choice == 1:
            login()
        elif choice == 2:
            sign_up()
        elif choice == 3:
            running = False
        else:
            print("Invalid Choice")
            print()
            continue
    
if __name__ == "__main__":
    main()
