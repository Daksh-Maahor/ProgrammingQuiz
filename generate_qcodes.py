import pickle

def generate():
    QUESTIONS_ALL = []
    with open('data/questions.bin', 'rb') as f:
        "print('Start')"
        data = pickle.load(f)
        QUESTIONS_ALL = data['questions_list']
        CONCEPTS = data['concepts_list']
        
        for i in QUESTIONS_ALL:
            type = i["type"]
            level = i["level"]
            concepts = i["concepts"]
            question = i["question"]
            options = i["options"]
            correct_option = i["correct_option"]
            
            hash = []
            
            mod = (len(type) + len(level) + len(question) + len(correct_option))
            
            for c in concepts:
                mod += len(c)
            
            for o in options:
                mod += len(o)
            
            mod = str((((mod * 7877 + 7621) * 7829 + 7753) * 7237 + 6883) * 7741 + 7547)
            for c in concepts:
                hash += [c[int(mod[5]) % len(c)]]
            
            hash += question[int(mod[3]) % len(question)]
            
            for o in options:
                hash += [o[int(mod[6]) % len(o)]]
            
            hash += [correct_option[int(mod[7]) % len(correct_option)]]
                
            hash = [type[0], level[0]] + hash
                
            hash = ''.join(hash)
            hash = hash.replace(' ', '_')

            i['hash'] = hash
        
    obj = {'concepts_list': CONCEPTS, 'questions_list' : QUESTIONS_ALL}

    with open('data/questions.bin', 'wb') as f:
        pickle.dump(obj, f)
        
    f.close()
    
if __name__ == "__main__":
    generate()
