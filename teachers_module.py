import json
import mysql.connector
import __init__ as sql
import teacher_login_module as admin

USER_NAME = None
PASSWORD = None

def main():
    print("----   Programming Quiz   ----")
    print("----   Teacher's Module   ----")

    print()
    
    running = True
    
    while running:

        print("Select An Option")
        print("1. Login")
        print("2. Sign Up")
        print("3. Change Password")
        print("4. Log Out")
        print("5. Quit")

        choice = input(">> ")
        
        if not choice.isnumeric():
            print("Invalid Choice")
            print()
            continue
        
        choice = int(choice)

        if choice == 1:
            #login()
            pass
        elif choice == 2:
            #sign_up()
            pass
        elif choice == 3:
            #update_passkey()
            pass
        elif choice == 4:
            #log_out()
            pass
        elif choice == 5:
            running = False
        else:
            print("Invalid Choice")
            print()
            continue
    
if __name__ == "__main__":
    main()

