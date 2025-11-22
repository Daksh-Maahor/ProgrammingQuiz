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

