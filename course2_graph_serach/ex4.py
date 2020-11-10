from typing import Dict


file = 'ex4_data.txt'
t_range = range(-10000, 10001)

data: Dict[int, int] = {}

with open(file, 'r') as f:
    for line in f:
        val = int(line.strip())
        if val not in data:
            data[val] = val

counter = 0
for t in t_range:
    for key in data.keys():
        lookup_key = t - key
        if (lookup_key in data) and (lookup_key != key):
            counter += 1
            break
        else:
            continue

print(counter)

