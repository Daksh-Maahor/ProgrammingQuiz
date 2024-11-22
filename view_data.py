import pickle
import clear_data_module
from clear_data_module import CDM_CHOICE_DATA_CLEAR, CDM_CHOICE_SELECTED_DATA_CLEAR

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

def main(choiceee, passwd=None):
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

                with open('data/admins.bin', 'rb') as f:

                    data = pickle.load(f)
                    print(type(data))
                    print(f"Num of admins {len(data)}")
                    pretty_print_list(data)

                print('\n\n\n')

            elif choice == 2:

                print("Students Data : ")

                with open('data/students.bin', 'rb') as f:
                    data = pickle.load(f)
                    print(type(data))
                    print(f"Num of students {len(data)}")
                    pretty_print_list(data)

                print('\n\n\n')

            elif choice == 3:

                print("Questions Data : ")

                with open('data/questions.bin', 'rb') as f:
                    data = pickle.load(f)
                    print(type(data))
                    pretty_print(data)

                print("\n\n\n")

            elif choice == 4:

                print("User Statistics : ")

                with open("data/user_stats.bin", 'rb') as f:
                    data = pickle.load(f)
                    print(type(data))
                    pretty_print_list(data)
            else:
                print("Invalid choice")
    elif choiceee == VM_CHOICE_DATA_CLEAR:
        clear_data_module.main(CDM_CHOICE_DATA_CLEAR, passwd)
    elif choiceee == VM_CHOICE_SELECTED_DATA_CLEAR:
        clear_data_module.main(CDM_CHOICE_SELECTED_DATA_CLEAR, passwd)

if __name__ == "__main__":
    print("Select : ")
    print("1. View Data")
    print("2. Clear Whole Data")
    print("3. Clear Specific Entries")

    choiceee = input(">> ")

    if not choiceee.isnumeric():
        print("Invalid Choice")
    else:
        choiceee = int(choiceee)

        main(choiceee)
