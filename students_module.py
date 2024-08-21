import json
import random
import __init__
import students_login_module as admin

        
USER_NAME = None
PASSWORD = None
        
def main():
    global USER_NAME, PASSWORD
    
    print("----   Programming Quiz   ----")
    print("----   Student's Module   ----")
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
        print("1. Login")
        print("2. Sign Up")
        print("3. Change Password")
        print("4. Log Out")
        print("5. Quit")
        
        if signed_in:
            print("6. Play Quiz")
            
        print()

        choice = input(">> ")
        
        if not choice.isnumeric():
            print("Invalid Choice")
            print()
            continue
        
        choice = int(choice)

        if choice == 1:
            if not signed_in:
                USER_NAME, PASSWORD = admin.login()
                signed_in = True
            else:
                print(f"You are already signed in as {USER_NAME}")
                print("Log Out First")
        elif choice == 2:
            admin.sign_up()
        elif choice == 3:
            PASSWORD = admin.update_passkey()
        elif choice == 4:
            # log_out
            signed_in = False
            USER_NAME = None
            PASSWORD = None
        elif choice == 5:
            running = False
        elif choice == 6:
            if signed_in:
                #PLAY QUIZ HERE
                
                pass
            else:
                print("Invalid Choice")
                print()
                continue
        else:
            print("Invalid Choice")
            print()
            continue
    
    

if __name__ == "__main__":
    main()
    
    
    