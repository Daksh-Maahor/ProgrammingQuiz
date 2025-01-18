import common_login_module as admin
from common_login_module import STUDENTS_DATABASE
import quiz_module as quiz
import pickle
        
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
                USER_NAME, PASSWORD = admin.login(STUDENTS_DATABASE)
                signed_in = True
            else:
                print(f"You are already signed in as {USER_NAME}")
                print("Log Out First")
        elif choice == 2:
            admin.sign_up(STUDENTS_DATABASE)
        elif choice == 3:
            PASSWORD = admin.update_passkey(STUDENTS_DATABASE)
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
                        '''
                        i["Analysis"]["times"].update(analysis["times"])
                        i["Analysis"]["accuracy"].update(analysis["accuracy"])
                        i["Analysis"]["level_report"].update(analysis["level_report"])
                        i["Analysis"]["type_report"].update(analysis["type_report"])
                        i["Analysis"]["overall_report"].update(analysis["overall_report"])
                        '''
                        '''for j in analysis["correct_que_ids"]:
                            if j in i["Analysis"]["incorrect_que_ids"]:
                                i["Analysis"]["incorrect_que_ids"].remove(j)
                            if not j in i["Analysis"]["correct_que_ids"]:
                                i["Analysis"]["correct_que_ids"].append(j)

                        for j in analysis["incorrect_que_ids"]:
                            if j in i["Analysis"]["correct_que_ids"]:
                                i["Analysis"]["correct_que_ids"].remove(j)
                            if not j in i["Analysis"]["incorrect_que_ids"]:
                                i["Analysis"]["incorrect_que_ids"].append(j)'''
                if not found:
                    new_data = {"User_name" : USER_NAME, "Analysis" : [analysis]}
                    data.append(new_data)

                with open("data/user_stats.bin", 'wb') as f:
                    pickle.dump(data, f)
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
    
    
    