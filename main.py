import pygame
import json
import random
import __init__

pygame.init()
pygame.font.init()

"""

Programming Quiz Game something

Creator : Daksh Maahor The Great

Reason for Creation : CBSE + khudki curiosity + Charu mam ki advice

App Name : Not yet decided (whoever tells a good name will win $1 million)

Aim of the application : To help fellow students remember python concepts 
                         in an interactive way or something

Made in : Python 3.12.3 + JSON

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
NUM_QUESTIONS_IN_QUIZ = 2

'QUESTION LEVELS'

LEVEL_EASY = 'EASY'
LEVEL_MEDIUM = 'MEDIUM'
LEVEL_HARD = 'HARD'
LEVELS_QUE = [LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD]

'QUESTION TYPES'

TYPE_MCQ = 'MCQ'
#TYPE_ONE_WORD = 'ONE_WORD'
TYPES_QUE = [TYPE_MCQ,] #TYPE_ONE_WORD]

'RENDER QUESTION PARAMETERS'

MAX_WIDTH = 600
FPS = 60

'Colors'

COLOR_WHITE = 255, 255, 255
COLOR_BLACK = 0, 0, 0
COLOR_GRAY_DARK = 64, 64, 64
COLOR_GRAY_LIGHT = 128, 128, 128

'VARS'

SIZE = 640
BTN_WIDTH = 200
BTN_HEIGHT = 50

WIN = pygame.display.set_mode((SIZE, SIZE))

NUM_CHAR_BEFORE_SPACE = 30   # for question rendering
                             # no of chars before new line

'FONTS'

FONT = pygame.font.SysFont('comicsans', 30)
SFONT = pygame.font.SysFont('comicsans', 20)

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
    with open('questions.json', 'rt') as f:
        "print('Start')"
        QUESTIONS_ALL = json.load(f)['questions_list']
        """print(QUESTIONS_ALL)
        print('\n')"""
        
        '''for question in QUESTIONS_LIST:
            if (len(question["question"]) > NUM_CHAR_BEFORE_SPACE):
                i = len(question["question"]) // NUM_CHAR_BEFORE_SPACE
                
                for j in range(i):
                    if question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1))-1] != ' ' and question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1))] != ' ':
                        question["question"] = question["question"][:(NUM_CHAR_BEFORE_SPACE*(j+1))] + '-\n' + question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1)):]
                    else:
                        question["question"] = question["question"][:(NUM_CHAR_BEFORE_SPACE*(j+1))] + '\n' + question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1)):]'''
        'print(QUESTIONS_LIST)'
        
        print("Questions: \n\n")
        
        for j, i in enumerate(QUESTIONS_ALL):
            print(j)
            pretty_print(i)
            print()
    QID_LIST = [i['hash'] for i in QUESTIONS_ALL]
    pretty_print_list(QID_LIST, 'QIDs')
    f.close()
    
    l = len(QUESTIONS_ALL)
    
    for question in QUESTIONS_ALL:
        # question display formatting
        if (len(question["question"]) > NUM_CHAR_BEFORE_SPACE):
            i = len(question["question"]) // NUM_CHAR_BEFORE_SPACE
            
            for j in range(i):
                if question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1))-1] != ' ' and question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1))] != ' ':
                    question["question"] = question["question"][:(NUM_CHAR_BEFORE_SPACE*(j+1))] + '-\n' + question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1)):]
                else:
                    question["question"] = question["question"][:(NUM_CHAR_BEFORE_SPACE*(j+1))] + '\n' + question["question"][(NUM_CHAR_BEFORE_SPACE*(j+1)):]
    
    if l <= NUM_QUESTIONS_IN_QUIZ:
        
        QUESTIONS_LIST = QUESTIONS_ALL
    else:
        '''i = 1 # to count index of que we are currently at
        j = 0 # to count no of questions added
        
        QUESTIONS_ALL = random.shuffle(QUESTIONS_ALL)
        
        for ques in QUESTIONS_ALL:
            chance = random.randrange(1, 101)
            
            p_factor =       # fancy name for threshold (probability factor)
        '''
        
        q_list = [i for i in QUESTIONS_ALL]
        QUESTIONS_LIST = []
        
        j = 0 # to keep track of questions taken
        
        while j < NUM_QUESTIONS_IN_QUIZ:
            i = random.randrange(0, len(q_list))
            QUESTIONS_LIST.append(q_list[i])
            
            q_list.pop(i)
            
            random.shuffle(q_list)
            j += 1
    
    print('\nQUESTIONS : \n')
    
    for que in QUESTIONS_LIST:
        pretty_print(que, 1)
        print()

# to render text on screen
def text_objects(text : str, surfaceH = 200):
    paragraphSize = (MAX_WIDTH, surfaceH)
    fontSize = FONT.get_height()

    # Step 1
    paragraphSurface = pygame.Surface(paragraphSize) 

    #Set colorkey to fake transparent paragraph surface
    paragraphSurface.fill((255, 255, 255))
    paragraphSurface.set_colorkey((255, 255, 255))

    # Step 2
    splitLines = text.splitlines()
    
    #Step 4
    for idx, line in enumerate(splitLines):
        currentTextline = FONT.render(line, 1, (0, 0, 0))
        currentPostion = ((paragraphSize[0] - currentTextline.get_width()) // 2, idx * fontSize)
        paragraphSurface.blit(currentTextline, currentPostion)

    #Step 5
    return paragraphSurface

#print score analysis        
def display_analysis(quiz_state):
    'print(quiz_state.analysis)'
    pretty_print(quiz_state.analysis)
    
def update_frame(keys, mouseClicked, mousePos):
    CURRENT_STATE.update(keys, mouseClicked, mousePos)
    
    pygame.display.update()

'STATE SWITCH FUNCTIONS'

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
        to_exit_state()
        
'Classes'
    
class Button:
    def __init__(self, func, rect, text='', col_a=COLOR_GRAY_DARK, col_b=COLOR_GRAY_LIGHT) -> None:
        self.func = func
        self.rect = rect
        self.col_a = col_a
        self.col_b = col_b
        self.text = text
        
    def onMouseClick(self, mousePos):
        if (self.rect.collidepoint(mousePos[0], mousePos[1])):
            "print(f'Clicked on button {self}')"
            return self.func()
        
    def render(self, mousePos):
        if (self.rect.collidepoint(mousePos[0], mousePos[1])):
            pygame.draw.rect(WIN, self.col_a, self.rect)
        else:
            pygame.draw.rect(WIN, self.col_b, self.rect)
        WIN.blit((line := SFONT.render(self.text, True, COLOR_WHITE)), (self.rect[0] + (self.rect[2] - line.get_width())/2, self.rect[1] + (self.rect[3] - line.get_height())/2, line.get_width(), line.get_height()))
    
class MenuState:
    def __init__(self) -> None:
        self.buttons = []
        self.counter = 0
        
        self.buttons.append(Button(to_game_state, pygame.rect.Rect((SIZE - BTN_WIDTH) // 2, (SIZE - BTN_HEIGHT) // 2, BTN_WIDTH, BTN_HEIGHT), 'Start'))
        
    def update(self, keys, mouseClicked, mousePos):
        global NAME
        if mouseClicked:
            for btn in self.buttons:
                _ = btn.onMouseClick(mousePos)
        
        if self.counter == 7:
            for i in range(32, 123):
                if i > 32 and i < 97:
                    continue
                
                if i in keys:
                    if not keys[i]:
                        continue
                    
                    NAME += chr(i)
                    
            if pygame.K_BACKSPACE in keys:
                if keys[pygame.K_BACKSPACE]:
                    NAME = NAME[:-1]
                    
            self.counter = 0
        
        self.counter += 1
        
        WIN.fill(COLOR_WHITE)
        
        'print(NAME)'
        text = NAME+'_'
        WIN.blit((line:= FONT.render(text, True, COLOR_BLACK)), pygame.rect.Rect((SIZE - line.get_width())//2, (SIZE - 200 - line.get_height())//2, line.get_width(), line.get_height()))
        
        for btn in self.buttons:
            btn.render(mousePos)
            

class Question:
    def __init__(self, number, level, concepts_used, question, hash) -> None:
        self.number = number
        self.level = level
        self.concepts_used = concepts_used
        self.question = question
        self.time_taken = 0
        self.type = ''
        self.hash = hash
        
    def update(self, keys, mouseClicked, mousePos):
        self.time_taken += 1/FPS
    
    def render(self, keys, mouseClicked, mousePos):
        print("Render function not defined in this class")
        
class MCQ(Question):
    def __init__(self, number, level, concepts_used, question, options, correct_option, hash) -> None:
        super().__init__(number, level, concepts_used, question, hash)
        self.options = options
        self.type = 'MCQ'
        self.correct_option = correct_option
        
        self.buttons = []
        
        for i, option in enumerate(self.options):
            if option == self.correct_option:
                self.buttons.append(Button(quiz_state_next_right, pygame.rect.Rect((SIZE // 4 * ((i % 2) * 2 + 1)) - BTN_WIDTH // 2, (300 + 200 * (i // 2)) - BTN_HEIGHT // 2, BTN_WIDTH, BTN_HEIGHT), option))
            else:
                self.buttons.append(Button(quiz_state_next_wrong, pygame.rect.Rect((SIZE // 4 * ((i % 2) * 2 + 1)) - BTN_WIDTH // 2, (300 + 200 * (i // 2)) - BTN_HEIGHT // 2, BTN_WIDTH, BTN_HEIGHT), option))
        
    def update(self, keys, mouseClicked, mousePos):
        super().update(keys, mouseClicked, mousePos)
        if mouseClicked:
            for btn in self.buttons:
                _ = btn.onMouseClick(mousePos)
        
    def render(self, keys, mouseClicked, mousePos):
        WIN.blit(text_objects(f'Q{self.number}. {self.question}'), pygame.rect.Rect((SIZE - MAX_WIDTH)//2, 100, SIZE, 200))
        
        for btn in self.buttons:
            btn.render(mousePos)
        
    def __repr__(self) -> str:
        return f'( {self.number}, {self.level}, {self.concepts_used}, {self.question}, {self.options} )'

class QuizState:
    def __init__(self) -> None:
        self.buttons = []
        
        self.current_que_no = 0
        
        
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
        
        'print("Printing from quizState: ", self.questions)'
        
    def update(self, keys, mouseClicked, mousePos):
        'print(self.current_que_no)'
        if mouseClicked:
            for btn in self.buttons:
                _ = btn.onMouseClick(mousePos)
                
        self.questions[self.current_que_no].update(keys, mouseClicked, mousePos)
        
        WIN.fill(COLOR_WHITE)
        
        for btn in self.buttons:
            btn.render(mousePos)
            
        self.questions[self.current_que_no].render(keys, mouseClicked, mousePos)

class ResultState:
    def __init__(self, quiz_state) -> None:
        self.quiz_state = quiz_state
        self.buttons = []
        self.i = 0
    
    def update(self, keys, mouseClicked, mousePos):
        global NAME
        if mouseClicked:
            for btn in self.buttons:
                _ = btn.onMouseClick(mousePos)
        
        WIN.fill(COLOR_WHITE)
        
        for btn in self.buttons:
            btn.render(mousePos)
            
        # TODO : Show result
        
        NAME = NAME.lower().replace(' ', '_')
        
        if self.i == 0:
            print("\n\n")
            display_analysis(self.quiz_state)
            data = {}
            f = None
            try:
                with open('users/'+NAME+'.json', 'rt') as f:
                    data = json.load(f)
                    q_wise_analysis = data['Quewise_Analysis']
                    q_new_analysis = []
                    for id in QID_LIST:
                        id_dict = {'QID' : id}
                        
                        # 1 == COrrect response
                        # 0 == Incorrect response
                        # -1 == not attempted yet
                        if id in self.quiz_state.right_ids:
                            id_dict['response_correct'] = 1
                        elif id in self.quiz_state.wrong_ids:
                            id_dict['response_correct'] = 0
                        else:
                            for i in q_wise_analysis:
                                if i['QID'] == id:
                                    id_dict['response_correct'] = i['response_correct']
                            
                        if id in self.quiz_state.times:
                            id_dict['time_taken'] = self.quiz_state.times[id]
                        else:
                            for i in q_wise_analysis:
                                if i['QID'] == id:
                                    id_dict['time_taken'] = i['time_taken']
                        
                        for i in QUESTIONS_ALL:
                            if i['hash'] == id:
                                id_dict['level'] = i['level']
                                
                    
                        '''for id in self.quiz_state.right_ids:
                            if id in data['wrong_ids']:
                                data['wrong_ids'].pop(id)
                                data['right_ids'].append(id)
                            elif id not in data['right_ids']:
                                data['right_ids'].append(id)
                            
                        for id in self.quiz_state.wrong_ids:
                            if id in data['right_ids']:
                                data['right_ids'].pop(id)
                                data['wrong_ids'].append(id)
                            elif id not in data['wrong_ids']:
                                data['wrong_ids'].append(id)'''
                        
                        q_new_analysis.append(id_dict)
                        
                    data['Quewise_Analysis'] = q_new_analysis
                
                f.close()
                
                with open('users/'+NAME+'.json', 'wt') as f:
                    '''data = {}
                    
                    data['name'] = NAME
                    
                    data['right_ids'] = self.quiz_state.right_ids
                    data['wrong_ids'] = self.quiz_state.wrong_ids'''
                    
                    json.dump(data, f, indent=4)
                
                f.close()
            except:
                with open('users/'+NAME+'.json', 'wt') as f:
                    '''data = {}
                    
                    data['name'] = NAME
                    
                    data['right_ids'] = self.quiz_state.right_ids
                    data['wrong_ids'] = self.quiz_state.wrong_ids'''
                    
                    data = {}
                    
                    data['name'] = NAME
                    
                    q_wise_analysis = []
                    
                    for id in QID_LIST:
                        id_dict = {'QID' : id}
                        
                        # 1 == COrrect response
                        # 0 == Incorrect response
                        # -1 == not attempted yet
                        if id in self.quiz_state.right_ids:
                            id_dict['response_correct'] = 1
                        elif id in self.quiz_state.wrong_ids:
                            id_dict['response_correct'] = 0
                        else:
                            id_dict['response_correct'] = -1
                            
                        if id in self.quiz_state.times:
                            id_dict['time_taken'] = self.quiz_state.times[id]
                        else:
                            id_dict['time_taken'] = 0.0
                        
                        for i in QUESTIONS_ALL:
                            if i['hash'] == id:
                                id_dict['level'] = i['level']
                        
                        q_wise_analysis.append(id_dict)
                        
                    data['Quewise_Analysis'] = q_wise_analysis
                    
                    '''for id in self.quiz_state.right_ids:
                        if id in data['wrong_ids']:
                            data['wrong_ids'].pop(id)
                            data['right_ids'].append(id)
                        elif id not in data['right_ids']:
                            data['right_ids'].append(id)
                        
                    for id in self.quiz_state.wrong_ids:
                        if id in data['right_ids']:
                            data['right_ids'].pop(id)
                            data['wrong_ids'].append(id)
                        elif id not in data['wrong_ids']:
                            data['wrong_ids'].append(id)'''
                    
                    
                    json.dump(data, f, indent=4)
                
                f.close()
                
            f.close()
            
            'Place holder code below'
            'Not deleting yet, will delete for final draft'
                
            # try:
            #     with open('users/'+NAME+'.json', 'rt') as f:
            #         data = json.load(f)
                    
            #         for id in QID_LIST:
            #             id_dict = {'QID' : id}
                        
            #             # 1 == COrrect response
            #             # 0 == Incorrect response
            #             # -1 == not attempted yet
            #             if id in self.quiz_state.right_ids:
            #                 id_dict['response_correct'] = 1
            #             elif id in self.quiz_state.wrong_ids:
            #                 id_dict['response_correct'] = 0
            #             else:
            #                 id_dict['response_correct'] = -1
                    
            #         '''for id in self.quiz_state.right_ids:
            #             if id in data['wrong_ids']:
            #                 data['wrong_ids'].pop(id)
            #                 data['right_ids'].append(id)
            #             elif id not in data['right_ids']:
            #                 data['right_ids'].append(id)
                        
            #         for id in self.quiz_state.wrong_ids:
            #             if id in data['right_ids']:
            #                 data['right_ids'].pop(id)
            #                 data['wrong_ids'].append(id)
            #             elif id not in data['wrong_ids']:
            #                 data['wrong_ids'].append(id)'''
                            
            #     with open('users/'+NAME+'.json', 'wt') as f:
            #         '''data = {}
                    
            #         data['name'] = NAME
                    
            #         data['right_ids'] = self.quiz_state.right_ids
            #         data['wrong_ids'] = self.quiz_state.wrong_ids'''
                    
            #         json.dump(data, f, indent=4)
                
            #     f.close()
            # except:
            #     with open('users/'+NAME+'.json', 'wt') as f:
            #         data = {}
                    
            #         '''data['name'] = NAME
                    
            #         data['right_ids'] = self.quiz_state.right_ids
            #         data['wrong_ids'] = self.quiz_state.wrong_ids
                    
            #         json.dump(data, f, indent=4)'''
                    
            #         data['name'] = NAME
                    
            #         data['qwise_analysis'] = []
                    
            #         for id in QID_LIST:
            #             id_dict = {'QID' : id}
                        
            #             # 1 == COrrect response
            #             # 0 == Incorrect response
            #             # -1 == not attempted yet
            #             if id in self.quiz_state.right_ids:
            #                 id_dict['response_correct'] = 1
            #             elif id in self.quiz_state.wrong_ids:
            #                 id_dict['response_correct'] = 0
            #             else:
            #                 id_dict['response_correct'] = -1
                        
            #             if id in self.quiz_state.times:
            #                 id_dict['time_taken'] = self.quiz_state.times[id]
            #             else:
            #                 id_dict['time_taken'] = 0.0
                
            #     f.close()
                
        self.i += 1
        if self.i > 100:
            self.i = 1
        
        WIN.blit((text:=FONT.render("Result", True, COLOR_BLACK)), pygame.rect.Rect((SIZE - text.get_width())//2, (SIZE - text.get_height())//2, text.get_width(), text.get_height()))

'''
def main():
    running = True
    mousePos = 0, 0
    mouseClicked = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
                
        update_frame()
    
    pygame.quit()'''
    
def main():
    global CURRENT_STATE, NAME
    # NAME = input("Enter your Name : ").replace(' ', '_').lower()
    running = True
    clock = pygame.time.Clock()
    
    mouseClicked = False
    mousePos = 0, 0
    
    keys = {}
    
    while running:
        clock.tick(FPS)
        mouseClicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys[event.key] = True
            elif event.type == pygame.KEYUP:
                keys[event.key] = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    mouseClicked = True
            elif event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
                'print(mousePos)'
                
        update_frame(keys, mouseClicked, mousePos)
        'pretty_print(keys)'
        'print()'
        
    pygame.quit()

if __name__ == "__main__":
    load_questions()
            
    MENU_STATE = MenuState()
    QUIZ_STATE = QuizState()
    RESULT_STATE = ResultState(QUIZ_STATE)

    CURRENT_STATE = MENU_STATE
    main()#lesgooooo
