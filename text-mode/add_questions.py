import json
import colorama
from termcolor import colored
from config import QuestionsTableConfig
from init_sql import get_db_connection

colorama.init()

def add_que(teacher_id):
    print(colored("==== Add Questions to the Quiz ====", 'light_magenta'))

    connection, cursor = get_db_connection()

    # Fetch existing concepts from the database
    cursor.execute(f"SELECT concepts FROM {QuestionsTableConfig.QUESTIONS_TABLE}")
    existing_concepts = []
    for row in cursor.fetchall():
        if row[0]:
            concept_list = row[0]
            for concept in json.loads(concept_list):
                if concept not in existing_concepts:
                    existing_concepts.append(concept)
    CONCEPTS_LIST = list(set([concepts for concepts in existing_concepts]))

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
    
    concepts = []
    
    print(colored("Select suitable concepts to be applied : (one or more numbers separated by space)", 'cyan'))
    print("If the concept you want is not listed, you can add it in the next step.")
    print("Just type 'end' to finish selecting from the list.")
    print("Available Concepts : ")
    for i, conc in enumerate(CONCEPTS_LIST):
        print(f"{i+1}. {conc}")
    
    indices = input(colored(">> ", 'green')).split(" ")
    
    for i in indices:
        if i.isnumeric():
            i = int(i)
            if i <= len(CONCEPTS_LIST) and i > 0:
                concepts.append(CONCEPTS_LIST[i-1])
    
    print()
    
    print(colored("Enter additional concepts not in previous list : (each concept in a new line, end by typing 'end')", 'cyan'))
    inp = input(colored(">> ", 'green'))
    while inp.lower().strip() != 'end':
        inp = inp.title()
        concepts.append(inp)
        
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
    
    print(colored("Enter correct option number : (1, 2, 3, 4)", "cyan"))
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
    
    # Insert the question into the database
    options = json.dumps([op1, op2, op3, op4])
    cursor.execute(
        f"INSERT INTO {QuestionsTableConfig.QUESTIONS_TABLE} ({QuestionsTableConfig.MENTOR_ID}, {QuestionsTableConfig.QUESTION_TEXT}, {QuestionsTableConfig.OPTIONS}, {QuestionsTableConfig.CORRECT_ANSWER}, {QuestionsTableConfig.DIFFICULTY}, {QuestionsTableConfig.CONCEPTS}) VALUES (%s, %s, %s, %s, %s, %s)",
        (teacher_id, question, options, corr_opt, level, json.dumps(concepts))
    )
    connection.commit()
    
    print(colored("Question added successfully!", 'green'))
    
        
        