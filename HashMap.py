# Oxi 17/01/22
import hashlib

class HashMapPair(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.collisionrefs = []
        self.owncollisions = []

        # COLLISIONS: where two keys get calculated to the same location. They should be bumped to the next available location, and referenced for lookups
        # collisionrefs: items that have been knocked by item being there
        # owncollisions: item that has knocked self by being there

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
                dr = 1
                while not validPos:
                    # Calculate location using offset from original hash
                    offset+=dr
                    newPos=self.calcpos(hashed+offset)
                    
                    # If within store bounds
                    if newPos[0] > 0 and newPos[0] < self.size and newPos[1] > 0 and newPos[1] < self.size:
                        # If no pair is taking up location
                        if self.store[newPos[0]][newPos[1]] == None:
                            validPos = True
                    if newPos[0] < 0:
                        if self.debug:
                            print(f"Map is full.")
                            return
                    elif newPos[0] >= self.size:
                        dr = -1

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
        # Calculate true location O(1)
        hashed = self.hashstr(key)
        x, y = self.calcpos(hashed)

        if self.store[x][y] == None:
            if self.debug:
                print(f"Key {key} ({hashed} - X:{x},Y:{y}) does not contain a value.")
        else:
            # Check if found object has correct key
            if self.store[x][y].key == key:
                return ((x,y), self.store[x][y].val)
            else:
                # Key would have to have collided, so find in collision references O(n)
                for refPos in self.store[x][y].collisionrefs:
                    # If correct Key
                    if self.store[refPos[0]][refPos[1]].key == key:
                        # Return correct pair
                        return ((refPos[0], refPos[1]), self.store[refPos[0]][refPos[1]].val)

                # Did not find collided key - must not have been addee
                if self.debug:
                    print(f"Key {key} ({hashed} - X:{x},Y:{y}) does not reference collided key (has not been entered).")

    def Remove(self, key):
        try:
            # Find key location, traversing collision references
            pos = self.Find(key)[0]
            x,y = pos

            if self.store[x][y] == None:
                if self.debug:
                    print(f"Key {key} (X:{x},Y:{y}) does not contain any value.")
            else:
                # Remove references to key being deleted
                for reference in self.store[x][y].owncollisions:
                    self.store[reference[0]][reference[1]].collisionrefs.remove((x,y))

                # Move references if any has collided with key being deleted
                if len(self.store[x][y].collisionrefs) > 0:
                    
                    # Find primary collided key to be moved to key being deleted location
                    newPrimary = self.store[x][y].collisionrefs[0]
                    
                    # For each object that has been collided by THAT key
                    for primaryRef in self.store[newPrimary[0]][newPrimary[1]].collisionrefs:
                        
                        # if new primary object is in their references, replace it with the new location
                        if newPrimary in self.store[primaryRef[0]][primaryRef[1]].owncollisions:
                            index = self.store[primaryRef[0]][primaryRef[1]].owncollisions.index(newPrimary)
                            self.store[primaryRef[0]][primaryRef[1]].owncollisions[index] = (x,y)

                    # Transfer collision refs (minus primary)
                    self.store[newPrimary[0]][newPrimary[1]].collisionrefs = self.store[x][y].collisionrefs[1:]
                    
                    # Move new primary in map store
                    self.store[x][y] = self.store[newPrimary[0]][newPrimary[1]]
                    self.store[newPrimary[0]][newPrimary[1]] = None

                    # Remove old key being deleted ref from new primary
                    self.store[x][y].owncollisions.remove((x,y))
                else:
                    # Else, empty slot
                    self.store[x][y] = None
        except:
            if self.debug:
                print(f"Failed to delete key {key}. Key was not found")

    def GetKeys(self):
        final = []
        for level1 in self.store:
            sublevel = []
            for item in level1:
                if not item == None:
                    final.append(item.key)
        return final

    def GetValues(self):
        final = []
        for key in self.GetKeys():
            final.append(self.Find(key)[1])
        return final

    def Clear(self):
        self.store = [[None]*self.size for i in range(self.size)]
        if self.debug:
            print("Cleared map")

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
        
