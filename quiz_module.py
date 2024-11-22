import pickle
import random
import time

"""

Programming Quiz Game something

Creator : Daksh Maahor The Great

Reason for Creation : CBSE + khudki curiosity + Charu mam ki advice

App Name : Not yet decided (whoever tells a good name will win $1 million)

Aim of the application : To help fellow students remember python concepts 
                         in an interactive way or something

Made in : Python 3.12.3 + SQL

"""

"""

Leaving the work here for now

Current Features:

    Quiz
    Progress tracker (storing in a file)
    Progress updater
    Personalised storage of data
    Auto updation each time the quiz is taken
    Basic entry based on name system ----> To be updated (priority)

To do list:

    Maybe split the code in multiple files
    (Although I won't do it coz I'm lazy and also single file me lagta hai ki insaan ne
     mehnat ki hai)

    Decide a name for program
    Make a Logo for program
    Add more questions
    Add personalized question finder
    
    Add a score system   <----- Current priority
    Also add login and register system    <----- Current priority
    
    (For above two use file with user name as file name to store 
              data about user response like no of corrext ans, and time taken etc : Done)
    Update : File storage done, personalization remains
    
    Add ability to restart without closing : Not seeming possible but will try
    
    baaki ka baad me dekh lenge :)
    har time ki performance dekhni hai -- growth of student
    time limit bhi rakhni hai
    time store karke analyse bhi karna hai
    admin, user, teacher modulefirst page--->login with category
    - user, admin ya teacher
    question add karne ka access teacher ko bhi dena hai
    first page ke baad -subject aur topic 
    then ask if user wants to review previous performance 
    admin ke paas user ki id, questions aur saari cheezein edit karne ka access
    teacher should have students' list
    teacher ke paas paper editing ka access hona chahiye 
    student ke paas topicwise evaluation ka access hona chahiye
    teacher ke paas individual performances honi chahiye har bacche ki 

"""

# IMPORTANT VARIABLES / CONSTANTS

'Player name'
NAME = ''

'load questions'

QUESTIONS_LIST = None # to be used in program

QUESTIONS_ALL = None # List of all questions

QID_LIST = None

#Total no of questions to be taken out of the database
NUM_QUESTIONS_IN_QUIZ = 4

'QUESTION LEVELS'

LEVEL_EASY = 'EASY'
LEVEL_MEDIUM = 'MEDIUM'
LEVEL_HARD = 'HARD'
LEVELS_QUE = [LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD]

'QUESTION TYPES'

TYPE_MCQ = 'MCQ'
#TYPE_ONE_WORD = 'ONE_WORD'
TYPES_QUE = [TYPE_MCQ,] #TYPE_ONE_WORD]

'UTILITY FUNCTIONS'

# to print the data in dictionaries
def pretty_print(dictionary, indent=0):
    for i in dictionary:
        print("    "*indent + str(i), ":")
        j = dictionary[i]
        if type(j) == dict:
            pretty_print(j, indent+1)
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
            
# to load questions
def load_questions():
    global QUESTIONS_LIST, QUESTIONS_ALL, QID_LIST
    QUESTIONS_ALL = []
    with open('data/questions.bin', 'rb') as f:
        QUESTIONS_ALL = pickle.load(f)['questions_list']
        
        """print("Questions: \n\n")
        
        for j, i in enumerate(QUESTIONS_ALL):
            print(j)
            pretty_print(i)
            print()"""
    QID_LIST = [i['hash'] for i in QUESTIONS_ALL]
    #pretty_print_list(QID_LIST, 'QIDs')
    f.close()
    
    l = len(QUESTIONS_ALL)
    
    if l <= NUM_QUESTIONS_IN_QUIZ:
        QUESTIONS_LIST = QUESTIONS_ALL
    else:
        q_list = [i for i in QUESTIONS_ALL]
        QUESTIONS_LIST = []
        
        j = 0 # to keep track of questions taken
        
        while j < NUM_QUESTIONS_IN_QUIZ:
            i = random.randrange(0, len(q_list))
            QUESTIONS_LIST.append(q_list[i])
            
            q_list.pop(i)
            
            random.shuffle(q_list)
            j += 1
    
    #print('\nQUESTIONS : \n')
    
    """for que in QUESTIONS_LIST:
        pretty_print(que, 1)
        print()"""
        
#print score analysis        
def display_analysis(quiz_state):
    'print(quiz_state.analysis)'
    pretty_print(quiz_state.analysis)
    
"""'STATE SWITCH FUNCTIONS'

def to_game_state():
    global CURRENT_STATE, QUIZ_STATE
    
    CURRENT_STATE = QUIZ_STATE
    
def to_exit_state():
    global CURRENT_STATE, RESULT_STATE
    
    for ques in QUIZ_STATE.questions:
        QUIZ_STATE.times[ques.hash]=round(ques.time_taken * 100)/100
    
    QUIZ_STATE.analysis["times"] = QUIZ_STATE.times
    QUIZ_STATE.analysis["accuracy"] = QUIZ_STATE.accuracy
    QUIZ_STATE.analysis["lvl_report"] = QUIZ_STATE.que_level_report
    QUIZ_STATE.analysis["type_report"] = QUIZ_STATE.que_type_report
    QUIZ_STATE.analysis["overall_report"] = QUIZ_STATE.overall_report
    QUIZ_STATE.analysis["right_ids"] = QUIZ_STATE.right_ids
    QUIZ_STATE.analysis["wrong_ids"] = QUIZ_STATE.wrong_ids
    
    CURRENT_STATE = RESULT_STATE
    
def quiz_state_next_wrong():
    global QUIZ_STATE
    QUIZ_STATE.accuracy[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].hash]=False
    QUIZ_STATE.que_level_report[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].level]["incorrect"] += 1
    QUIZ_STATE.que_type_report[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].type]["incorrect"] += 1
    QUIZ_STATE.overall_report["incorrect"] += 1
    QUIZ_STATE.wrong_ids.append(QUIZ_STATE.questions[QUIZ_STATE.current_que_no].hash)
    if QUIZ_STATE.current_que_no < len(QUIZ_STATE.questions) - 1:
        QUIZ_STATE.current_que_no += 1
    else:
        to_exit_state()
    
def quiz_state_next_right():
    global QUIZ_STATE
    QUIZ_STATE.accuracy[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].hash]=True
    QUIZ_STATE.que_level_report[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].level]["correct"] += 1
    QUIZ_STATE.que_type_report[QUIZ_STATE.questions[QUIZ_STATE.current_que_no].type]["correct"] += 1
    QUIZ_STATE.overall_report["correct"] += 1
    QUIZ_STATE.right_ids.append(QUIZ_STATE.questions[QUIZ_STATE.current_que_no].hash)
    if QUIZ_STATE.current_que_no < len(QUIZ_STATE.questions) - 1:
        QUIZ_STATE.current_que_no += 1
    else:
        to_exit_state()"""
        

'Classes'

class Question:
    def __init__(self, number, level, concepts_used, question, hash) -> None:
        self.number = number
        self.level = level
        self.concepts_used = concepts_used
        self.question = question
        self.time_taken = 0
        self.type = ''
        self.hash = hash
        
    def render() -> bool:
        print("Render function not defined in this class")
        return False
        
class MCQ(Question):
    def __init__(self, number, level, concepts_used, question, options, correct_option, hash) -> None:
        super().__init__(number, level, concepts_used, question, hash)
        self.options = options
        self.type = 'MCQ'
        self.correct_option = correct_option
        
    def render(self) -> bool: # prints the question and returns whether the answer was correct or not
        print(f'Q{self.number}. {self.question}')
        random.shuffle(self.options)
        
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option}")
            
        print("Enter option (1, 2, 3, 4)")
        
        ans = input(">> ")
        
        if not ans.isnumeric():
            return False
        
        ans = int(ans)
        
        if 1 <= ans <= 4:
            return self.options[ans-1] == self.correct_option
        else:
            return False
        
    def __repr__(self) -> str:
        return f'( {self.number}, {self.level}, {self.concepts_used}, {self.question}, {self.options} )'
    
####

    """

        TODO:
        
        Store Quiz accuracy according to various parameters (que difficulty, que type etc)
    
    """

####
class QuizState:
    def __init__(self, stu_name) -> None:
        self.stu_name = stu_name
        
        
        self.questions = []
        
        self.times = {}
        self.accuracy = {}
        
        self.analysis = {}
        self.que_level_report = dict.fromkeys(LEVELS_QUE)
        self.que_type_report = dict.fromkeys(TYPES_QUE)
        self.overall_report = {"correct" : 0, "incorrect" : 0}
        
        self.wrong_ids = []
        self.right_ids = []
        
        for lvl in LEVELS_QUE:
            self.que_level_report[lvl] = {"correct" : 0, "incorrect" : 0}
        
        for qtype in TYPES_QUE:
            self.que_type_report[qtype] = {"correct" : 0, "incorrect" : 0}
        
        for question in QUESTIONS_LIST:
            que = None
            if question['type'] == 'MCQ':
                que = MCQ(0, question['level'], question['concepts'], question['question'], question['options'], question['correct_option'], question['hash'])
                
            self.questions.append(que)
            
        'print(self.questions)'
        
        random.shuffle(self.questions)
        
        for i, question in enumerate(self.questions):
            question.number = i+1
        
        #print("Printing from quizState: ", self.questions)
        
    def render(self):
        for i in self.questions:
            t1 = round(time.time_ns() / 1000000000, 2)
            correct = i.render()
            t2 = round(time.time_ns() / 1000000000, 2)

            self.times[i.hash] = round(t2 - t1, 2)
            self.accuracy[i.hash] = correct
            
            if correct:
                self.right_ids.append(i.hash)
                self.overall_report["correct"] += 1
                self.que_level_report[i.level]["correct"] += 1
                self.que_type_report[i.type]["correct"] += 1
            else:
                self.wrong_ids.append(i.hash)
                self.overall_report["incorrect"] += 1
                self.que_level_report[i.level]["incorrect"] += 1
                self.que_type_report[i.type]["incorrect"] += 1
        
        self.analysis["times"] = self.times
        self.analysis["accuracy"] = self.accuracy
        self.analysis["level_report"] = self.que_level_report
        self.analysis["type_report"] = self.que_type_report
        self.analysis["overall_report"] = self.overall_report
        self.analysis["correct_que_ids"] = self.right_ids
        self.analysis["incorrect_que_ids"] = self.wrong_ids
        
        display_analysis(self)
        return self.analysis
                
            
        
def play(STU_NAME):
    load_questions()
    quiz = QuizState(STU_NAME)
    return quiz.render()

if __name__ == "__main__":
    play("")
    