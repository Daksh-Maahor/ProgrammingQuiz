import traceback
import pickle


def update_admins_and_students():
    file_data = []
    with open("data/admins.bin", "rb") as f:
        try:
            file_data = pickle.load(f)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    with open("data/admins.bin", 'wb') as f:
        try:
            
            user_names = []
            admins = []
            for i in file_data:
                if not i['Username'] in user_names:
                    admins.append({"Username" : i['Username'], "Password" : i['Password']})
                    user_names.append(i['Username'])
            
            
            pickle.dump(admins, f)
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    file_data = []
    with open("data/students.bin", "rb") as f:
        try:
            file_data = pickle.load(f)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    
    with open("data/students.bin", 'wb') as f:
        try:
            
            user_names = []
            students = []
            for i in file_data:
                if not i['Username'] in user_names:
                    students.append({"Username" : i['Username'], "Password" : i['Password']})
                    user_names.append(i['Username'])
            
            
            pickle.dump(students, f)
            
        except Exception as err:
            traceback.print_tb(err.__traceback__)
    

update_admins_and_students()
