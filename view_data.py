import pickle
import clear_data_module
from clear_data_module import CDM_CHOICE_DATA_CLEAR, CDM_CHOICE_SELECTED_DATA_CLEAR
from prettytable import PrettyTable
import init_sql

STUDENTS_DATABASE = "students_login_data"
TEACHERS_DATABASE = "teachers_login_data"

VM_CHOICE_DATA_VIEW = 1
VM_CHOICE_DATA_CLEAR = 2
VM_CHOICE_SELECTED_DATA_CLEAR = 3

# to print the data in dictionaries
def pretty_print(dictionary, indent=0):
    for i in dictionary:
        print("    "*indent + str(i), ":")
        j = dictionary[i]
        if type(j) == dict:
            pretty_print(j, indent+1)
        elif type(j) == list:
            pretty_print_list(j, indent=indent+1)
        else:
            print("    "*(indent+1) + str(j))
            
# to print data in lists
def pretty_print_list(lst, title='', indent=0):
    print('    '*(indent), title, ":\n")
    for i in lst:
        if type(i) == list:
            pretty_print_list(i, indent=indent+1)
        elif type(i) == dict:
            pretty_print(i, indent+1)
        else:
            print('   '*(indent+1), i)

def view_students_performance(user_name):
    with open("data/user_stats.bin", 'rb') as f:
        data = pickle.load(f)
        l = []
        for i in data:
            if i["Mentor_name"] == user_name:
                l.append(i)
        
    print("Select Student")

    for i, j in enumerate(l):
        print(f"{i+1}. {j["User_name"]}")
    
    idx = input(">> ")
    if idx.isnumeric():
        idx = int(idx) - 1
        if idx >= len(l) or idx < 0:
            print(f"Index out of range (1-{len(l)})")
        else:

            data = l[idx]
            analysises = data["Analysis"]

            for i, analysis in enumerate(analysises):
                print(f"Attempt {i + 1}")

                print("Overall Report : ")
                data = analysis["overall"]
                print()

                overall_data_table = PrettyTable(["Total Questions", "Correct", "Incorrect"])
                overall_data_table.add_row([data["correct"] + data["incorrect"], data["correct"], data["incorrect"]])

                print(overall_data_table)

                print()
                print()

                data = analysis["q_wise"]
                print("Question Wise Report")
                qwise_data_table = PrettyTable(["QID", "Question", "Time", "Accuracy", "Level", "Key Concepts"])
                for d in data:
                    qwise_data_table.add_row([d["QID"], d["Question"], d["Time"], "Correct" if d["Accuracy"] else "Incorrect", d["Level"], d["Key Concepts"]])
                    qwise_data_table.add_row(["", "", "", "", "", ""])
                
                print(qwise_data_table)

                print()
                print()

    else:
        print("Invalid Input")

def main(choiceee, CURSOR, connect, passwd=None):
    if choiceee == VM_CHOICE_DATA_VIEW:

        print("Select : ")
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(">> ")

        if not choice.isnumeric():
            print("Invalid choice")
        else:
            choice = int(choice)
            if choice == 1:

                print("Admins Data : ")

                CURSOR.execute(f"SELECT * FROM {TEACHERS_DATABASE}")
                admins_table = PrettyTable(["Mentor Name", "Password"])

                data = CURSOR.fetchall()

                for entry in data:
                    admins_table.add_row(entry)

                print(admins_table)

                print('\n\n\n')

            elif choice == 2:

                print("Students Data : ")

                CURSOR.execute(f"SELECT * FROM {STUDENTS_DATABASE}")
                students_table = PrettyTable(["Student Name", "Password", "Mentor Name"])

                data = CURSOR.fetchall()

                for entry in data:
                    students_table.add_row(entry)

                print(students_table)

                print('\n\n\n')

            elif choice == 3:

                print("Questions Data : ")

                with open('data/questions.bin', 'rb') as f:
                    data = pickle.load(f)

                    list_concepts = data["concepts_list"]
                    concepts_table = PrettyTable()
                    concepts_table.add_column("Concepts", list_concepts)
                    print(concepts_table)

                    print()
                    print()

                    print("Questions List")

                    list_qns = data["questions_list"]
                    qns_table = PrettyTable(["Q. No.", "Question", "Options", "Level", "Concepts"])
                    for i, qn in enumerate(list_qns):
                        qns_table.add_row([i+1, qn["question"], qn["options"], qn["level"], qn["concepts"]])
                        qns_table.add_row(["", "", "", "", ""])
                    
                    print(qns_table)
                    print()
                    print()

                print("\n\n\n")

            elif choice == 4:

                print("User Statistics : ")

                with open("data/user_stats.bin", 'rb') as f:
                    data = pickle.load(f)
                    
                    for i in data:
                        print(f"Student Name : {i["User_name"]}")
                        print(f"Mentor Name : {i["Mentor_name"]}")

                        analysises = i["Analysis"]

                        for j, analysis in enumerate(analysises):
                            print(f"Attempt {j + 1}")

                            print("Overall Report : ")
                            data = analysis["overall"]
                            print()

                            overall_data_table = PrettyTable(["Total Questions", "Correct", "Incorrect"])
                            overall_data_table.add_row([data["correct"] + data["incorrect"], data["correct"], data["incorrect"]])

                            print(overall_data_table)

                            print()
                            print()

                            data = analysis["q_wise"]
                            print("Question Wise Report")
                            qwise_data_table = PrettyTable(["QID", "Question", "Time", "Accuracy", "Level", "Key Concepts"])
                            for d in data:
                                qwise_data_table.add_row([d["QID"], d["Question"], d["Time"], "Correct" if d["Accuracy"] else "Incorrect", d["Level"], d["Key Concepts"]])
                                qwise_data_table.add_row(["", "", "", "", "", ""])
                            
                            print(qwise_data_table)

                            print()
                            print()

                
                    '''print(type(data))
                    pretty_print_list(data)'''
            else:
                print("Invalid choice")
    elif choiceee == VM_CHOICE_DATA_CLEAR:
        clear_data_module.main(CDM_CHOICE_DATA_CLEAR, passwd)
    elif choiceee == VM_CHOICE_SELECTED_DATA_CLEAR:
        clear_data_module.main(CDM_CHOICE_SELECTED_DATA_CLEAR, passwd)

def init():
    print("Select : ")
    print("1. View Data")
    print("2. Clear Whole Data")
    print("3. Clear Specific Entries")

    choiceee = input(">> ")

    if not choiceee.isnumeric():
        print("Invalid Choice")
    else:
        choiceee = int(choiceee)
        CURSOR, connect = init_sql.init()
        main(choiceee, CURSOR, connect)

        init_sql.close()

if __name__ == "__main__":
    init()
