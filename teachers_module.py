import common_login_module as admin
from init_sql import TEACHERS_DATABASE, STUDENTS_DATABASE
import add_questions as que_add
import view_data
from view_data import VM_CHOICE_DATA_VIEW, VM_CHOICE_DATA_CLEAR, VM_CHOICE_SELECTED_DATA_CLEAR

USER_NAME = None
PASSWORD = None

def main(CURSOR, connect):
    global USER_NAME, PASSWORD
    print("----   Programming Quiz   ----")
    print("----   Teacher's Module   ----")
    print()
    print()

    print()
    
    running = True
    
    signed_in = False
    
    while running:
        
        if USER_NAME == None or PASSWORD == None:
            print("Currently Signed Out")
            signed_in = False
        else:
            print(f"Currently Signed In as {USER_NAME}")
            signed_in = True
            
        print()
        print()

        print("Select An Option")
        if not signed_in:
            print("1. Login")
            print("2. Sign Up")
            print("3. Quit")
            
        if signed_in:
            print("1. Change Password")
            print("2. Register Student")
            print("3. Add New Question")
            print("4. View Student Perfoormance")
            print("5. Log Out")
            print("6. Quit")
        
        print()

        choice = input(">> ")
        
        if not choice.isnumeric():
            print("Invalid Choice")
            print()
            continue
        
        choice = int(choice)

        if not signed_in:
            if choice == 1: # sign in
                USER_NAME, _, PASSWORD = admin.login(TEACHERS_DATABASE, CURSOR)
                signed_in = True
            elif choice == 2: # sign up
                admin.sign_up(TEACHERS_DATABASE, CURSOR, connect)
            elif choice == 3:
                running = False
            else:
                print("Invalid Choice")
                print()
                continue
        
        elif signed_in:
            if choice == 1:
                PASSWORD = admin.update_passkey(TEACHERS_DATABASE, USER_NAME, CURSOR, connect)
            elif choice == 2:
                admin.sign_up(STUDENTS_DATABASE, CURSOR, connect, USER_NAME)
            elif choice == 3:
                que_add.add_que()
            elif choice == 4:
                view_data.view_students_performance(USER_NAME)
            elif choice == 5:
                signed_in = False
                USER_NAME = None
                PASSWORD = None
            elif choice == 6:
                running = False
            else:
                print("Invalid Choice")
                print()
                continue
