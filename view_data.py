import pickle

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

print("Admins Data : ")

with open('data/admins.bin', 'rb') as f:
    data = pickle.load(f)
    print(type(data))
    pretty_print_list(data)

print('\n\n\n')

print("Students Data : ")

with open('data/students.bin', 'rb') as f:
    data = pickle.load(f)
    print(type(data))
    pretty_print_list(data)

print('\n\n\n')

print("Questions Data : ")

with open('data/questions.bin', 'rb') as f:
    data = pickle.load(f)
    print(type(data))
    pretty_print(data)

print("\n\n\n")

print("User Statistics : ")

with open("data/user_stats.bin", 'rb') as f:
    data = pickle.load(f)
    print(type(data))
    pretty_print_list(data)
