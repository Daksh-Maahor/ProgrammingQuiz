import json
import pickle

with open("users/daksh_maahor.json", 'rt') as f:
    data = json.load(f)

with open('data/user_stats.bin', 'wb') as f:
    pickle.dump(data, f)
