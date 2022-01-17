from HashMap import *

# For each array size, calculate the maximum hashed digits that can be used
# This is basically trying to see whats the maximum amount of digits that can be wrapped around to fit within the array size of x:size y:size

s = 10
prev = 0
while s < 10001:
    hashmap = HashMap(s)

    d = 100
    fin = False
    while d > 1 and not fin:
        a = "999999999999999999999999999999999999999999999"
        pos = hashmap.calcpos(int(a[:d]))
        if pos[0] < s:
            if not prev == d:
                print(f"For size {s}, max digits is {d}: ({int(a[:d])}), X:{pos[0]}, Y:{pos[1]}")
                prev = d
            fin = True
        d-=1

    s = s + 1

