import common_login_module as admin
from init_sql import TEACHERS_DATABASE, STUDENTS_DATABASE
import add_questions as que_add
import view_data
import colorama
from termcolor import colored

colorama.init()

USER_NAME = None
PASSWORD = None

def main(CURSOR, connect):
    global USER_NAME, PASSWORD
    print(colored("----       Quiz           ----", 'green'))
    print(colored("----   Teacher's Module   ----", 'green'))
    print()
    print()

    print()
    
    running = True
    
    signed_in = False
    
    while running:
        
        if USER_NAME == None or PASSWORD == None:
            print(colored("Currently Signed Out", 'light_magenta'))
            signed_in = False
        else:
            print(colored(f"Currently Signed In as {USER_NAME}", 'light_magenta'))
            signed_in = True
            
        print()
        print()

        print(colored("Select An Option", 'cyan'))
        if not signed_in:
            print("1. Login")
            print("2. Sign Up")
            print("3. Quit")
            
        if signed_in:
            print("1. Change Password")
            print("2. Register Student")
            print("3. Add New Question")
            print("4. View My Students")
            print("5. View Student Performance")
            print("6. View Quiz")
            print("7. Log Out")
            print("8. Delete Account")
            print("9. Quit")
        
        print()

        choice = input(colored(">> ", 'green'))
        
        if not choice.isnumeric():
            print(colored("Invalid Choice", 'red'))
            print()
            continue
        
        choice = int(choice)

        if not signed_in:
            if choice == 1: # sign in
                USER_NAME, _, PASSWORD = admin.login(TEACHERS_DATABASE, CURSOR)
                signed_in = True
            elif choice == 2: # sign up
                success = admin.sign_up(TEACHERS_DATABASE, CURSOR, connect)
                if not success == False:
                    USER_NAME, _, PASSWORD = success
                    signed_in = True
            elif choice == 3:
                running = False
            else:
                print(colored("Invalid Choice", 'red'))
                print()
                continue
        
        elif signed_in:
            if choice == 1:
                PASSWORD = admin.update_passkey(TEACHERS_DATABASE, USER_NAME, CURSOR, connect)
            elif choice == 2:
                admin.sign_up(STUDENTS_DATABASE, CURSOR, connect, USER_NAME)
            elif choice == 3:
                que_add.add_que(USER_NAME)
            elif choice == 4:
                view_data.view_students(USER_NAME, CURSOR)
            elif choice == 5:
                view_data.view_students_performance(USER_NAME)

            elif choice == 6:
                view_data.view_quiz(USER_NAME)
            elif choice == 7:
                signed_in = False
                USER_NAME = None
                PASSWORD = None
            elif choice == 8:
                view_data.delete_account(USER_NAME, CURSOR, connect, TEACHERS_DATABASE)
                USER_NAME = None
                PASSWORD = None
                signed_in = False
            elif choice == 9:
                running = False
            else:
                print(colored("Invalid Choice", 'red'))
                print()
                continue
