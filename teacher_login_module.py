import pickle
import __init__ as sql


def login() -> tuple[str, str]:  # returns (username, password). None in both if login fails.
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()

    with open("data/admins.bin", 'rb') as f:
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

def sign_up(): # returns Nothing. as registration does not confirm login
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()

    with open("data/admins.bin", 'rb') as f:
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
        with open("data/admins.bin", 'wb') as f:
            pickle.dump(data_reg, f)
        print()
        print()
    else:
        print(f"User ID {user_name} already exists.")
        print()
        print()
        return
    
def update_passkey() -> str: # returns password, as that's what has changed
    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = input(">> ")
    print()
    
    if len(data) == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
        return pass_key
    else:
        data = data[0]
        if pass_key != data[1]:
            print("Invalid Password")
            print()
            print()
            return pass_key
        else:
            print("Enter new Password : ")
            pass_key = input(">> ")
            
            sql.connect.commit()
            print("Password Changed Successfully!")
            print()
            print()
            
            data = []
            
            with open("data/admins.bin", 'rb') as f:
                data = pickle.load(f)
                
            for i in data:
                if i["Username"] == user_name:
                    i["Password"] = pass_key
                    break
            
            with open("data/admins.bin", 'wb') as f:
                pickle.dump(data, f, indent=4)
            
            return pass_key

