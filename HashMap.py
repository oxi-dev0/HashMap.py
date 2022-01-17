import hashlib

class HashMapPair(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.collisionrefs = []
        self.owncollisions = []

    def __str__(self):
        return f"{{'{self.key}': {self.val}, collisionrefs: {self.collisionrefs}, owncollisions: {self.owncollisions}}}"

# NOTES ON DYNAMIC SIZING: Need to be able to calculate the maximum number of digits the hash can use to fit in an
# array of size [size,size] when looped around using integer division and mod. I can do this recursively, but
# will get slower the bigger the hashmap needs to be, and also defeats the purpose of a Hashmap.
# It seems to switch on multiples of 10 and primes? (32 isnt prime, but is 2^5 if that is relevant)

# All calculated switching sizes
#For size 10, max digits is 2: (99), X:9, Y:9
#For size 32, max digits is 3: (999), X:31, Y:7
#For size 100, max digits is 4: (9999), X:99, Y:99
#For size 317, max digits is 5: (99999), X:315, Y:144
#For size 1000, max digits is 6: (999999), X:999, Y:999
#For size 3163, max digits is 7: (9999999), X:3161, Y:1756
#For size 10000, max digits is 8: (99999999), X:9999, Y:9999

class HashMap(object):
    def __init__(self, size=500, hashlength=5, debug=False):
        self.size = size
        self.hashlength = hashlength
        self.store = [[None]*self.size for i in range(self.size)]
        self.debug = debug

    def hashstr(self, string):
        # SHA256 Hash a string into a 5 digit integer. Calculate hash length dynamically soon.
        return int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16) % 10**self.hashlength

    def calcpos(self, hashed):
        # Calculate the array position using mod and remainder (effectively looping it) to constrain it to the 2D array size
        return (hashed // self.size, hashed % self.size)

    def Add(self, key, val):
        hashed = self.hashstr(key)
        x, y = self.calcpos(hashed)
        
        if self.store[x][y] == None:
            self.store[x][y] = HashMapPair(key, val)
        else:
            if self.store[x][y].key == key:
                # Overwrite
                self.store[x][y].val = val
            else:
                # COLLISION
                if self.debug:
                    print(f"COLLISION: '{key}' ({hashed}) with '{self.store[x][y].key}' ({self.hashstr(self.store[x][y].key)} - X:{x}, Y:{y})")

                # Find next available neighbour pos [WILL RUN INFINITELY IF BIGGER THAN ARRAY MAX]
                validPos = False
                newPos = (0,0)
                offset = 0
                while not validPos:
                    offset+=1
                    newPos=self.calcpos(hashed+offset)
                    if newPos[0] > 0 and newPos[0] < self.size and newPos[1] > 0 and newPos[1] < self.size:
                        if self.store[newPos[0]][newPos[1]] == None:
                            validPos = True

                if self.debug:
                    print(f"Found suitable redirect location: {{X:{newPos[0]}, Y:{newPos[1]}}}")

                # Make busy slot reference new collision slot
                self.store[x][y].collisionrefs.append(newPos)

                # Make new collision slot reference busy slot
                self.store[newPos[0]][newPos[1]] = HashMapPair(key, val)
                self.store[newPos[0]][newPos[1]].owncollisions.append((x,y))

                # collisionrefs: items that have been knocked by item being there
                # owncollisions: item that has knocked self by being there

    def Find(self, key):
        hashed = self.hashstr(key)
        x, y = self.calcpos(hashed)

        if self.store[x][y] == None:
            if self.debug:
                print(f"Key {key} ({hashed} - X:{x},Y:{y}) does not contain a value.")
        else:
            # Check if found object is correct
            if self.store[x][y].key == key:
                return ((x,y), self.store[x][y].val)
            else:
                # Find correct object
                for refPos in self.store[x][y].collisionrefs:
                    if self.store[refPos[0]][refPos[1]].key == key:
                        # Found collided correct object
                        return ((refPos[0], refPos[1]), self.store[refPos[0]][refPos[1]].val)

                # Did not find correct object
                if self.debug:
                    print(f"Key {key} ({hashed} - X:{x},Y:{y}) does not reference collided object (has not collided).")

    def Remove(self, key):
        try:
            pos = self.Find(key)[0]
            x,y = pos

            if self.store[x][y] == None:
                if self.debug:
                    print(f"Key {key} (X:{x},Y:{y}) does not contain any value.")
            else:
                # Remove references to self
                for reference in self.store[x][y].owncollisions:
                    self.store[reference[0]][reference[1]].collisionrefs.remove((x,y))

                # Move references if any has collided
                if len(self.store[x][y].collisionrefs) > 0:
                    
                    # Decide collided object to be moved to location
                    newPrimary = self.store[x][y].collisionrefs[0]
                    
                    # For each object that has been collided by THAT object
                    for primaryRef in self.store[newPrimary[0]][newPrimary[1]].collisionrefs:
                        
                        # if new primary object is in their references, replace it with the new location
                        if newPrimary in self.store[primaryRef[0]][primaryRef[1]].owncollisions:
                            index = self.store[primaryRef[0]][primaryRef[1]].owncollisions.index(newPrimary)
                            self.store[primaryRef[0]][primaryRef[1]].owncollisions[index] = (x,y)

                    # Transfer collision refs (minus primary)
                    self.store[newPrimary[0]][newPrimary[1]].collisionrefs = self.store[x][y].collisionrefs[1:]
                    
                    # Move actual new primary
                    self.store[x][y] = self.store[newPrimary[0]][newPrimary[1]]
                    self.store[newPrimary[0]][newPrimary[1]] = None

                    # Remove old ref from new primary
                    self.store[x][y].owncollisions.remove((x,y))
                else:
                    # Else, empty slot
                    self.store[x][y] = None
        except:
            if self.debug:
                print(f"Failed to delete key {key}. Object was not found")

    def DebugPrint(self):
        final = []
        for level1 in self.store:
            sublevel = []
            for item in level1:
                if item == None:
                    sublevel.append("None")
                else:
                    sublevel.append(str(item))
            final.append(f"[{', '.join(sublevel)}]")
        print(f"[{', '.join(final)}]")

   # def GetKeys(self):
        
