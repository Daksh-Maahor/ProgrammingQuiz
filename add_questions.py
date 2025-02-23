import generate_qcodes
import pickle
import colorama
from termcolor import colored

colorama.init()

def add_que(teacher_id):
    print(colored("==== Add Questions to the Quiz ====", 'light_magenta'))

    with open(f"data/{teacher_id}/questions.bin", 'rb+') as f:
        data = pickle.load(f)
        questions_list = data['questions_list']
        print()
        print(colored("Select Question Type", 'cyan'))
        print("1. MCQ")
        print(colored("Enter suitable number : ", 'cyan'))
        typee = input(colored(">> ", 'green'))
        if not typee.isnumeric():
            print(colored("Invalid Input", 'red'))
            return

        typee = int(typee)
        
        if typee == 1:
            typee = "MCQ"
        else:
            print(colored("Invalid Input", 'red'))
            return
        
        print()
        
        print(colored("Select Question Level", 'cyan'))
        print("1. EASY")
        print("2. MEDIUM")
        print("3. HARD")
        print(colored("Enter suitable number : ", 'cyan'))
        level = input(colored(">> ", 'green'))
        if not level.isnumeric():
            print(colored("Invalid Input", 'red'))
            return

        level = int(level)
        
        if level == 1:
            level = "EASY"
        elif level == 2:
            level = "MEDIUM"
        elif level == 3:
            level = "HARD"
        else:
            print(colored("Invalid Input", 'red'))
            return
        
        print()
        
        CONCEPTS_LIST = data["concepts_list"]
        
        concepts = []
        
        print(colored("Select suitable concepts to be applied : (one or more numbers separated by space)", 'cyan'))
        for i, conc in enumerate(CONCEPTS_LIST):
            print(f"{i+1}. {conc}")
        
        indices = input(colored(">> ", 'green')).split(" ")
        
        for i in indices:
            if i.isnumeric():
                i = int(i)
                if i < len(CONCEPTS_LIST) and i >= 0:
                    concepts.append(CONCEPTS_LIST[i-1])
        
        print()
        
        print(colored("Enter additional concepts not in previous list : (each concept in a new line, end by typing 'end')", 'cyan'))
        inp = input(colored(">> ", 'green'))
        while inp.lower().strip() != 'end':
            inp = inp.title()
            concepts.append(inp)
            CONCEPTS_LIST.append(inp)
            
            inp = input(colored(">> ", 'green'))
        
        print()
        
        print(colored("Enter Question :", 'cyan'))
        question = input(colored(">> ", 'green'))
        print()
        
        print(colored("Enter the Options :", 'cyan'))
        op1 = input(colored(">> ", 'green'))
        op2 = input(colored(">> ", 'green'))
        op3 = input(colored(">> ", 'green'))
        op4 = input(colored(">> ", 'green'))
        
        print()
        
        print(colored("Enter correct option : (1, 2, 3, 4)", "cyan"))
        corr_opt = input(colored(">> ", 'green'))
        if not corr_opt.isnumeric():
            print(colored("Invalid Input", 'red'))
            return
        
        corr_opt = int(corr_opt)
        if corr_opt == 1:
            corr_opt = op1
        elif corr_opt == 2:
            corr_opt = op2
        elif corr_opt == 3:
            corr_opt = op3
        elif corr_opt == 4:
            corr_opt = op4
        else:
            print(colored("Invalid Input", 'red'))
            return
        
        print()
        
        
        questions_list.append({"type" : typee, 
                               "level": level,
                               "concepts": concepts,
                               "question": question,
                               "options" : [op1, op2, op3, op4],
                               "correct_option" : corr_opt})
        
        data = {"concepts_list" : CONCEPTS_LIST, "questions_list" : questions_list}
    with open(f"data/{teacher_id}/questions.bin", 'wb') as f:
        pickle.dump(data, f)
        
    generate_qcodes.generate(teacher_id)
        
        