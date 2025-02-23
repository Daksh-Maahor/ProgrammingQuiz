import pickle
import random
import time as time_measure
import colorama
from termcolor import colored

colorama.init()

# Player name
NAME = ''

QUESTIONS_LIST = None # to be used in program

QUESTIONS_ALL = None # List of all questions

QID_LIST = None

#Total no of questions to be taken out of the database
NUM_QUESTIONS_IN_QUIZ = 10

# QUESTION LEVELS
LEVEL_EASY = 'EASY'
LEVEL_MEDIUM = 'MEDIUM'
LEVEL_HARD = 'HARD'
LEVELS_QUE = [LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD]

# QUESTION TYPES
TYPE_MCQ = 'MCQ'
TYPES_QUE = [TYPE_MCQ]

            
# to load questions
def load_questions(mentor_name):
    global QUESTIONS_LIST, QUESTIONS_ALL, QID_LIST
    QUESTIONS_ALL = []
    with open(f'data/{mentor_name}/questions.bin', 'rb') as f:
        QUESTIONS_ALL = pickle.load(f)['questions_list']
    
    QID_LIST = [i['hash'] for i in QUESTIONS_ALL]
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
        print(colored(f'Q{self.number}. {self.question}', 'cyan'))
        random.shuffle(self.options)
        
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option}")
            
        print(colored("Enter option (1, 2, 3, 4)", 'cyan'))
        
        while len(ans := input(colored(">> ", 'green'))) == 0:
            print(colored("Please enter your answer", 'red'))
        
        if not ans.isnumeric():
            return False
        
        ans = int(ans)
        
        if 1 <= ans <= 4:
            return self.options[ans-1] == self.correct_option
        else:
            return False
        
    def __repr__(self) -> str:
        return f'( {self.number}, {self.level}, {self.concepts_used}, {self.question}, {self.options} )'
    
class QuizState:
    def __init__(self, stu_name) -> None:
        self.stu_name = stu_name
        
        self.questions = []
        
        self.analysis = {"q_wise" : [], "overall" : {}}
        self.overall_report = {"correct" : 0, "incorrect" : 0}
        
        for question in QUESTIONS_LIST:
            que = None
            if question['type'] == 'MCQ':
                que = MCQ(0, question['level'], question['concepts'], question['question'], question['options'], question['correct_option'], question['hash'])
                
            self.questions.append(que)
            
        'print(self.questions)'
        
        random.shuffle(self.questions)
        
        for i, question in enumerate(self.questions):
            question.number = i+1
        
    def render(self):
        for i in self.questions:
            t1 = round(time_measure.time_ns() / 1000000000, 2)
            correct = i.render()
            t2 = round(time_measure.time_ns() / 1000000000, 2)

            time = round(t2 - t1, 2)
            accuracy = correct

            self.analysis["q_wise"].append({"QID" : i.hash, "Question" : i.question, "Time" : time, "Accuracy" : accuracy, "Level" : i.level, "Key Concepts" : i.concepts_used})
            
            if correct:
                self.overall_report["correct"] += 1
            else:
                self.overall_report["incorrect"] += 1
        
        self.analysis["overall"] = self.overall_report
        self.analysis["score"] = self.overall_report["correct"] / len(self.questions) * 100
        
        return self.analysis
                
def play(STU_NAME, MEN_NAME):
    load_questions(MEN_NAME)
    quiz = QuizState(STU_NAME)
    return quiz.render()

if __name__ == "__main__":
    play("")
    