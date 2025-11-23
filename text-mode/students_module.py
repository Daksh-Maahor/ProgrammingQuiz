import common_login_module as admin
from config import StudensTableConfig
import quiz_module as quiz
import view_data
import colorama
from termcolor import colored

colorama.init()

USER_NAME = None
PASSWORD = None
MENTOR_NAME = None

def main(cursor, connection):
    global USER_NAME, PASSWORD, MENTOR_NAME
    
    print(colored("----        Quiz          ----", 'green'))
    print(colored("----   Student's Module   ----", 'green'))
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
            print(colored(f"Currently Signed In as {USER_NAME}, student of {MENTOR_NAME}", 'light_magenta'))
            signed_in = True
            
        print()
        print()

        print(colored("Select An Option", 'cyan'))

        if not signed_in:
            print("1. Login")
            print("2. Quit")
        elif signed_in:
            print("1. Change Password")
            print("2. Play Quiz")
            print("3. Log Out")
            print("4. Delete Account")
            print("5. Quit")
        print()

        choice = input(colored(">> ", 'green'))
        
        if not choice.isnumeric():
            print(colored("Invalid Choice", 'red'))
            print()
            continue
        
        choice = int(choice)

        if not signed_in:
            if choice == 1:
                USER_NAME, MENTOR_NAME, PASSWORD = admin.login(StudensTableConfig.STUDENTS_TABLE, cursor)
                signed_in = True
            elif choice == 2:
                running = False
            else:
                print(colored("Invalid Choice", 'red'))
                print()
                continue
        
        elif signed_in:
            if choice == 1:
                PASSWORD = admin.update_passkey(StudensTableConfig.STUDENTS_TABLE, USER_NAME, cursor, connection)
            elif choice == 2:
                # Play quiz and store attempts in database
                quiz.play(USER_NAME, MENTOR_NAME)
            elif choice == 3:
                # log_out
                signed_in = False
                USER_NAME = None
                PASSWORD = None
            
            elif choice == 4:
                view_data.delete_account(USER_NAME, cursor, connection, StudensTableConfig.STUDENTS_TABLE)
                USER_NAME = None
                PASSWORD = None
                signed_in = False

            elif choice == 5:
                running = False
                USER_NAME = None
                PASSWORD = None
                signed_in = False
            
            else:
                print(colored("Invalid Choice", 'red'))
                print()
                continue
    