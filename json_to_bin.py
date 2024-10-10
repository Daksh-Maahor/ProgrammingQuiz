import json
import pickle

with open("questions.json", 'rt') as f:
    data = json.load(f)

with open('data/questions.bin', 'wb') as f:
    pickle.dump(data, f)
