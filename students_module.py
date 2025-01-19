import common_login_module as admin
from common_login_module import STUDENTS_DATABASE
import quiz_module as quiz
import pickle
        
USER_NAME = None
PASSWORD = None
MENTOR_NAME = None

def main():
    global USER_NAME, PASSWORD, MENTOR_NAME
    
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

        if not signed_in:
            print("1. Login")
            print("2. Quit")
        elif signed_in:
            print("1. Change Password")
            print("2. Play Quiz")
            print("3. Log Out")
            print("4. Quit")
        print()

        choice = input(">> ")
        
        if not choice.isnumeric():
            print("Invalid Choice")
            print()
            continue
        
        choice = int(choice)

        if not signed_in:
            if choice == 1:
                USER_NAME, MENTOR_NAME, PASSWORD = admin.login(STUDENTS_DATABASE)
                signed_in = True
            elif choice == 2:
                running = False
            else:
                print("Invalid Choice")
                print()
                continue
        
        elif signed_in:
            if choice == 1:
                PASSWORD = admin.update_passkey(STUDENTS_DATABASE, USER_NAME)
            elif choice == 2:
                #PLAY QUIZ HERE
                analysis = quiz.play(USER_NAME)
                try:
                    with open("data/user_stats.bin", 'rb') as f:
                        data = pickle.load(f)
                except:
                    data = []
                
                found = False
                for i in data:
                    if i["User_name"] == USER_NAME:
                        found = True
                        i["Analysis"].append(analysis)
                if not found:
                    new_data = {"User_name" : USER_NAME, "Mentor_name" : MENTOR_NAME,  "Analysis" : [analysis]}
                    data.append(new_data)

                with open("data/user_stats.bin", 'wb') as f:
                    pickle.dump(data, f)

            elif choice == 3:
                # log_out
                signed_in = False
                USER_NAME = None
                PASSWORD = None
            
            elif choice == 4:
                running = False
            
            else:
                print("Invalid Choice")
                print()
                continue
    