import pickle
import colorama
from termcolor import colored
import shutil
import getpass
from prettytable import PrettyTable

colorama.init()

STUDENTS_DATABASE = "students_login_data"
TEACHERS_DATABASE = "teachers_login_data"

CDM_CHOICE_DATA_CLEAR          = 1
CDM_CHOICE_SELECTED_DATA_CLEAR = 2

def pretty_print(dictionary, indent=0, index=False):
    for k, i in enumerate(dictionary):
        if index:
            print()
            print()
            print("    " * indent, f"{k}:")
        print("    "*indent + str(i), ":")
        j = dictionary[i]
        if type(j) == dict:
            pretty_print(j, indent+1)
        elif type(j) == list:
            pretty_print_list(j, indent=indent+1)
        else:
            print("    "*(indent+1) + str(j))

def pretty_print_list(lst, title='', indent=0, index=False):
    print('    '*(indent), title, ":\n")
    for j, i in enumerate(lst):
        if index:
            print()
            print()
            print("    " * indent, f"{j}:")

        if type(i) == list:
            pretty_print_list(i, indent=indent+1)
        elif type(i) == dict:
            pretty_print(i, indent+1)
        else:
            print('   '*(indent+1), i)

def delete_account(user_name, CURSOR, connect, database):
    if database == TEACHERS_DATABASE:
        CURSOR.execute(f'DELETE FROM {database} WHERE USER_NAME = "{user_name}"')
        connect.commit()
        CURSOR.execute(f'DELETE FROM {STUDENTS_DATABASE} WHERE MENTOR_NAME = "{user_name}"')
        connect.commit()

        shutil.rmtree(f'data/{user_name}', ignore_errors=True)
    else:
        CURSOR.execute(f'DELETE FROM {database} WHERE USER_NAME = "{user_name}"')
        connect.commit()

        CURSOR.execute(f'SELECT USER_NAME FROM {TEACHERS_DATABASE}')
        teachers_list = CURSOR.fetchall()

        for teacher_id in teachers_list:
            with open(f"data/{teacher_id[0]}/user_stats.bin", "rb") as f:
                data = pickle.load(f) # list
            
                idx = -1
                for i, j in enumerate(data):
                    if j['User_name'] == user_name:
                        idx = i
                if idx >= 0:
                    del data[idx]
                
            with open(f"data/{teacher_id[0]}/user_stats.bin", "wb") as f:
                pickle.dump(data, f) # list

def delete_questions(user_name, passwd):
    print(colored("Select : ", 'cyan'))
    print("1. Clear All Questions")
    print("2. Clear Selected Questions")

    choice = input(colored(">> ", 'green'))

    passs = getpass.getpass(colored("Enter password to continue : ", 'red'))

    if passs == passwd:
        if not choice.isnumeric():
            print(colored("Invalid Choice", 'red'))
        else:
            choice = int(choice)

            if choice == 1:
                with open(f'data/{user_name}/questions.bin', 'wb') as f:
                    pickle.dump({"concepts_list" : [], "questions_list" : []}, f)
            elif choice == 2:
                with open(f"data/{user_name}/questions.bin", "rb") as f:
                    data = pickle.load(f)
                    concepts = data["concepts_list"]
                    questions = data["questions_list"]

                print("Questions List")

                list_qns = data["questions_list"]
                qns_table = PrettyTable(["Q. No.", "Question", "Options", "Level", "Concepts"])
                for i, qn in enumerate(list_qns):
                    qns_table.add_row([i+1, qn["question"], qn["options"], qn["level"], qn["concepts"]])
                    qns_table.add_row(["", "", "", "", ""])
                
                print(qns_table)
                print()
                print()

                print(colored("Select an index to remove : ", 'cyan'))
                idx = input(colored(">> ", 'green'))

                if not idx.isnumeric():
                    print("Invalid Input")
                else:
                    idx = int(idx)

                    if idx < len(questions) and idx >= 0:
                        del questions[idx]
                    else:
                        print("Invalid index")

                with open(f"data/{user_name}/questions.bin", "wb") as f:
                    pickle.dump({"concepts_list" : concepts, "questions_list" : questions}, f) # list

    
'''def main(choiceeee, CURSOR, connect, passwd=None):
    if choiceeee == CDM_CHOICE_DATA_CLEAR:
        print(colored("Select : ", 'cyan'))
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(colored(">> ", 'green'))

        passss = None

        if passwd:
            passss = input("Re-enter password to confirm")

        if passss == passwd or not passwd:
            if not choice.isnumeric():
                print("Invalid Choice")
            else:
                choice = int(choice)

                if choice == 1:
                    CURSOR.execute(f'DELETE FROM {TEACHERS_DATABASE}')
                    connect.commit()
                
                elif choice == 2:
                    CURSOR.execute(f'DELETE FROM {STUDENTS_DATABASE}')
                    connect.commit()
                    with open("data/user_stats.bin", "wb") as f:
                        pickle.dump([], f)

                elif choice == 3:
                    with open("data/questions.bin", "wb") as f:
                        pickle.dump({"concepts_list" : [], "questions_list" : []}, f)
                
                elif choice == 4:
                    with open("data/user_stats.bin", "wb") as f:
                        pickle.dump([], f)
        else:
            print("Invalid Password. Terminated")
    elif choiceeee == CDM_CHOICE_SELECTED_DATA_CLEAR:
        print(colored("Select : ", 'cyan'))
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(colored(">> ", 'green'))

        passss = None

        if passwd:
            passss = input("Re-enter password to confirm")

        if passss == passwd or not passwd:
            if not choice.isnumeric():
                print("Invalid Choice")
            else:
                choice = int(choice)

                if choice == 1:

                    CURSOR.execute(f'SELECT * FROM {TEACHERS_DATABASE}')
                    data = CURSOR.fetchall()

                    pretty_print_list(data, "Admins List", index=True)

                    print()
                    print()
                    print(colored("Select an index to remove : ", "cyan"))
                    idx = input(colored(">> ", 'green'))

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(data) and idx >= 0:
                            user_name = data[idx][0]

                            CURSOR.execute(f'DELETE FROM {TEACHERS_DATABASE} WHERE USER_NAME="{user_name}"')
                            connect.commit()
                        else:
                            print("Invalid index")
                
                elif choice == 2:
                    CURSOR.execute(f'SELECT * FROM {STUDENTS_DATABASE}')
                    data = CURSOR.fetchall()

                    pretty_print_list(data, "Students List", index=True)

                    print()
                    print()
                    print("Select an index to remove : ")
                    idx = input(colored(">> ", 'green'))

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(data) and idx >= 0:
                            user_name = data[idx][0]

                            CURSOR.execute(f'DELETE FROM {STUDENTS_DATABASE} WHERE USER_NAME="{user_name}"')
                            connect.commit()

                            with open("data/user_stats.bin", "rb") as f:
                                data = pickle.load(f) # list
                            
                                idx = 0
                                for i, j in enumerate(data):
                                    if j['User_name'] == user_name:
                                        idx = i
                                        break

                                del data[idx]
                                
                            with open("data/user_stats.bin", "wb") as f:
                                pickle.dump(data, f) # list
                        else:
                            print("Invalid index")

                elif choice == 3:
                    with open("data/questions.bin", "rb") as f:
                        data = pickle.load(f)
                        concepts = data["concepts_list"]
                        questions = data["questions_list"]

                    pretty_print_list(questions, "Questions List", index=True)

                    print()
                    print()
                    print(colored("Select an index to remove : ", 'cyan'))
                    idx = input(colored(">> ", 'green'))

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(questions) and idx >= 0:
                            del questions[idx]
                        else:
                            print("Invalid index")

                    with open("data/questions.bin", "wb") as f:
                        pickle.dump({"concepts_list" : concepts, "questions_list" : questions}, f) # list
                
                elif choice == 4:
                    with open("data/user_stats.bin", "rb") as f:
                        data = pickle.load(f) # list

                    pretty_print_list(data, "User Statistics", index=True)

                    print()
                    print()
                    print(colored("Select an index to remove : ", 'cyan'))
                    idx = input(colored(">> ", 'green'))

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(data) and idx >= 0:
                            del data[idx]
                        else:
                            print("Invalid index")
                    
                    with open("data/user_stats.bin", "wb") as f:
                        pickle.dump(data, f) # list
        else:
            print("Invalid Password. Terminated")'''
