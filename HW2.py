import string
import random

def generate_dict(n):
    mydict = {}
    keys = set()  # To keep track of unique keys
    while len(keys) < n:
        key = random.choice(string.ascii_lowercase)
        if key not in keys:
            mydict[key] = random.randrange(100)
            keys.add(key)
    return mydict

l1 = []
for i in range(2, 11):
    l1.append(generate_dict(random.randrange(1, 10)))

common_dict = {}

for i, d in enumerate(l1):
    for key, value in d.items():
        if key in common_dict:
            # If the key already exists, update it
            if value > common_dict[key]:
                common_dict[key] = value
                # Rename the key with the dictionary number
                common_dict[f"{key}_{i + 1}"] = common_dict.pop(key)
        else:
            # If the key is unique, add it to the common dictionary
            common_dict[key] = value

print(common_dict)
