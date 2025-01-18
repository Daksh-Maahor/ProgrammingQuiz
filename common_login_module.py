import pickle
import getpass

STUDENTS_DATABASE = "data/students.bin"
TEACHERS_DATABASE = "data/admins.bin"

def login(database) -> tuple[str, str]:  # returns (username, password). None in both if login fails.

    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = getpass.getpass(">> ")
    print()

    with open(database, 'rb') as f:
        data = pickle.load(f)       # list

    matching = []

    for entry in data:
        if entry['Username'] == user_name:
            matching.append(entry)
    
    if len(matching) == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
    else:
        data = matching[0]
        if pass_key != data["Password"]:
            print("Invalid Password")
            print()
            print()
        else:
            print("Login Successful")
            print(f"Welcome {user_name}")
            print()
            print()
            
            return user_name, pass_key
    
    return None, None

def sign_up(database): # returns Nothing. as registration does not confirm login
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = getpass.getpass(">> ")
    print()

    with open(database, 'rb') as f:
        data = pickle.load(f)       # list

    matching = []

    for entry in data:
        if entry['Username'] == user_name:
            matching.append(entry)
    
    data_reg = data
    data = matching

    if len(data) == 0:
        print("Registration Successful.")
        data_reg.append({"Username" : user_name, "Password" : pass_key})
        with open(database, 'wb') as f:
            pickle.dump(data_reg, f)
        print()
        print()
    else:
        print(f"User ID {user_name} already exists.")
        print()
        print()
        return
    
def update_passkey(database) -> str: # returns password, as that's what has changed
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Old Password : ")
    pass_key = getpass.getpass(">> ")
    print()

    with open(database, 'rb') as f:
        data = pickle.load(f)       # list

    matching = []

    for entry in data:
        if entry['Username'] == user_name:
            matching.append(entry)
    
    data = matching
    
    if len(data) == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
        return pass_key
    else:
        data = data[0]
        if pass_key != data["Password"]:
            print("Invalid Password")
            print()
            print()
            return pass_key
        else:
            print("Enter new Password : ")
            pass_key = input(">> ")
            
            print("Password Changed Successfully!")
            print()
            print()
            
            data = []
            
            with open(database, 'rb') as f:
                data = pickle.load(f)
                
            for i in data:
                if i["Username"] == user_name:
                    i["Password"] = pass_key
                    break
            with open(database, 'wb') as f:
                pickle.dump(data, f)
            
            return pass_key

