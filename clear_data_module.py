import pickle

CDM_CHOICE_DATA_CLEAR = 1
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

def main(choiceeee, passwd=None):
    if choiceeee == CDM_CHOICE_DATA_CLEAR:
        print("Select : ")
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(">> ")

        passss = None

        if passwd:
            passss = input("Re-enter password to confirm")

        if passss == passwd or not passwd:
            if not choice.isnumeric():
                print("Invalid Choice")
            else:
                choice = int(choice)

                if choice == 1:
                    with open("data/admins.bin", "wb") as f:
                        pickle.dump([], f)
                
                elif choice == 2:
                    with open("data/students.bin", "wb") as f:
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
        print("Select : ")
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(">> ")

        passss = None

        if passwd:
            passss = input("Re-enter password to confirm")

        if passss == passwd or not passwd:
            if not choice.isnumeric():
                print("Invalid Choice")
            else:
                choice = int(choice)

                if choice == 1:
                    with open("data/admins.bin", "rb") as f:
                        data = pickle.load(f) # list

                    pretty_print_list(data, "Admins List", index=True)

                    print()
                    print()
                    print("Select an index to remove : ")
                    idx = input(">> ")

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(data) and idx >= 0:
                            del data[idx]
                        else:
                            print("Invalid index")
                    
                    with open("data/admins.bin", "wb") as f:
                        pickle.dump(data, f) # list
                
                elif choice == 2:
                    with open("data/students.bin", "rb") as f:
                        data = pickle.load(f) # list

                    pretty_print_list(data, "Students List", index=True)

                    print()
                    print()
                    print("Select an index to remove : ")
                    idx = input(">> ")

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx)

                        if idx < len(data) and idx >= 0:
                            del data[idx]
                        else:
                            print("Invalid index")
                    
                    with open("data/students.bin", "wb") as f:
                        pickle.dump(data, f) # list

                elif choice == 3:
                    with open("data/questions.bin", "rb") as f:
                        #pickle.dump({"concepts_list" : [], "questions_list" : []}, f)
                        data = pickle.load(f)
                        concepts = data["concepts_list"]
                        questions = data["questions_list"]

                    pretty_print_list(questions, "Questions List", index=True)

                    print()
                    print()
                    print("Select an index to remove : ")
                    idx = input(">> ")

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
                    print("Select an index to remove : ")
                    idx = input(">> ")

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
            print("Invalid Password. Terminated")
