import getpass

def login(database, CURSOR) -> tuple[str, str, str]:  # returns (username, mentor_name, password). None in both if login fails.

    print("Enter UserID : ")
    user_name = input(">> ")
    print("Enter Password : ")
    pass_key = getpass.getpass(">> ")
    print()

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
    else:
        data = CURSOR.fetchone()
        if pass_key != data[1]:
            print("Invalid Password")
            print()
            print()
        else:
            print("Login Successful")
            print(f"Welcome {user_name}")
            print()
            print()
            if len(data) == 3: # if mentor in data
                mentor_name = data[2]
                return user_name, mentor_name, pass_key
            return user_name, None, pass_key

    return None, None, None
    """with open(database, 'rb') as f:
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
            if "Mentor" in data:
                mentor_name = data["Mentor"]
                return user_name, mentor_name, pass_key
            return user_name, None, pass_key"""
    

def sign_up(database, CURSOR, connect, mentor_name=None): # returns Nothing. as registration does not confirm login

    print("Enter UserID : ")
    while len(user_name := input(">> ")) == 0:
        print("Please enter a valid username")
        print()
        print()

    print("Enter Password : ")
    while len(pass_key := getpass.getpass(">> ")) < 4:
        print("Password must be at least 4 characters")
        print()
        print()

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print("Registration Successful.")
        if mentor_name:
            CURSOR.execute(f'INSERT INTO {database}(USER_NAME, PASSWD, MENTOR_NAME) VALUES("{user_name}", "{pass_key}", "{mentor_name}")')
        else:
            CURSOR.execute(f'INSERT INTO {database}(USER_NAME, PASSWD) VALUES("{user_name}", "{pass_key}")')
        connect.commit()
        print()
        print()
    else:
        print(f"User ID {user_name} already exists.")
        print()
        print()
        return

    """
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
        if mentor_name:
            data_reg.append({"Username" : user_name, "Password" : pass_key, "Mentor" : mentor_name})
        else:
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
        """
    
def update_passkey(database, user_name, CURSOR, connect) -> str: # returns password, as that's what has changed
    print("Enter Old Password : ")
    pass_key = getpass.getpass(">> ")
    print()

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print(f"UserID {user_name} doesn't exist. Please Sign Up")
        print()
        print()
        return pass_key
    else:
        data = CURSOR.fetchone()
        if pass_key != data[1]:
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

            CURSOR.execute(f'UPDATE {database} SET PASSWD = "{pass_key}" WHERE USER_NAME = "{user_name}"')
            connect.commit()

            """
            data = []
            
            with open(database, 'rb') as f:
                data = pickle.load(f)
                
            for i in data:
                if i["Username"] == user_name:
                    i["Password"] = pass_key
                    break
            with open(database, 'wb') as f:
                pickle.dump(data, f)"""
            
            return pass_key

    """
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
    """

