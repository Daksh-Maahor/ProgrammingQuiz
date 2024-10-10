import generate_qcodes
import pickle
import __init__

def add_que():
    print("==== Add Questions to the Quiz ====")

    with open("data/questions.bin", 'rb+') as f:
        data = pickle.load(f)
        questions_list = data['questions_list']
        #print(questions_list)
        print()
        print("Select Question Type")
        print("1. MCQ")
        print("Enter suitable number : ")
        typee = input(">> ")
        if not typee.isnumeric():
            print("Invalid input")
            return

        typee = int(typee)
        
        if typee == 1:
            typee = "MCQ"
        else:
            print("Invalid Input")
            return
        
        print()
        
        print("Select Question Level")
        print("1. EASY")
        print("2. MEDIUM")
        print("3. HARD")
        print("Enter suitable number : ")
        level = input(">> ")
        if not level.isnumeric():
            print("Invalid input")
            return

        level = int(level)
        
        if level == 1:
            level = "EASY"
        elif level == 2:
            level = "MEDIUM"
        elif level == 3:
            level = "HARD"
        else:
            print("Invalid Input")
            return
        
        print()
        
        CONCEPTS_LIST = data["concepts_list"]
        
        concepts = []
        
        print("Select suitable concepts to be applied : (one or more numbers separated by space)")
        for i, conc in enumerate(CONCEPTS_LIST):
            print(f"{i+1}. {conc}")
        
        indices = input(">> ").split(" ")
        
        for i in indices:
            if i.isnumeric():
                i = int(i)
                if i < len(CONCEPTS_LIST) and i >= 0:
                    concepts.append(CONCEPTS_LIST[i])
        
        print()
        
        print("Enter additional concepts not in previous list : (each concept in a new line, end by typing 'end')")
        inp = input(">> ")
        while inp.lower().strip() != 'end':
            inp = inp.title()
            concepts.append(inp)
            CONCEPTS_LIST.append(inp)
            
            inp = input(">> ")
        
        print()
        
        print("Enter Question :")
        question = input(">> ")
        print()
        
        print("Enter the Options :")
        op1 = input(">> ")
        op2 = input(">> ")
        op3 = input(">> ")
        op4 = input(">> ")
        
        print()
        
        print("Enter correct option : (1, 2, 3, 4)")
        corr_opt = input(">> ")
        if not corr_opt.isnumeric():
            print("Invalid input")
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
            print("Invalid Input")
            return
        
        print()
        
        
        questions_list.append({"type" : typee, 
                               "level": level,
                               "concepts": concepts,
                               "question": question,
                               "options" : [op1, op2, op3, op4],
                               "correct_option" : corr_opt})
        
        data = {"concepts_list" : CONCEPTS_LIST, "questions_list" : questions_list}
        
        pickle.dump(data, f)
        
        generate_qcodes.generate()
        

if __name__ == "__main__":
    add_que()
        
        