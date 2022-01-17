from HashMap import *
import random

hashmap = HashMap(32, 3)

alpha = "abcdefghijklmnopqrstuwxyz"

def GenKey():
    final = ""
    for i in range(random.randrange(4, 15)):
        final += alpha[random.randrange(0, len(alpha)-1)]
    return final

found = False
while not found:
    key1 = GenKey()
    key2 = GenKey()
    key3 = GenKey()
    pos1 = hashmap.calcpos(hashmap.hashstr(key1))
    pos2 = hashmap.calcpos(hashmap.hashstr(key2))
    pos3 = hashmap.calcpos(hashmap.hashstr(key3))
    if pos1[0] == pos2[0] == pos3[0] and pos1[1] == pos2[1] == pos3[1]:
        print(f"COLLISION: '{key1}' and '{key2}' and '{key3}' at X:{pos1[0]} Y:{pos1[1]}")
