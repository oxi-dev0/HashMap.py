# Oxi 17/01/22
from HashMap import *

hashmap = HashMap(10, 2, True)

def onlyDigits(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def RunInstruction(instruction, params):
    global hashmap
    if instruction == "add":
        hashmap.Add(params[0], params[1])
        print(f"Added '{params[1]}' under key '{params[0]}' successfully.")
    elif instruction == "find":
        hashed = hashmap.hashstr(params[0])
        x, y = hashmap.calcpos(hashed)
        data = hashmap.Find(params[0])
        try:
            if x == data[0][0] and y == data[0][1]:
                print(f"'{params[0]}': Loc: {{X:{x}, Y:{y}}}, Value: {data[1]}")
            else:
                print(f"'{params[0]}': True Loc: {{X:{x}, Y:{y}}} - Rebounded to {{X:{data[0][0]}, Y:{data[0][1]}}}, Value: {data[1]}")
        except:
            print(f"Error finding '{params[0]}'")
    elif instruction == "remove":
        hashmap.Remove(params[0])
        print(f"Removed key '{params[0]}' successfully.")
    elif instruction == "position":
        pos = hashmap.calcpos(hashmap.hashstr(params[0]))
        print(f"Position of key '{params[0]}' is {{X:{pos[0]},Y:{pos[1]}}}")
    elif instruction == "hash":
        print(f"Hash of key '{params[0]}' is {hashmap.hashstr(params[0])}")
    elif instruction == "print":
        hashmap.DebugPrint()
    elif instruction == "keys":
        print(hashmap.GetKeys())
    elif instruction == "values":
        print(hashmap.GetValues())
    elif instruction == "clear":
        hashmap.Clear()
    elif instruction == "tofile":
        print(hashmap.ToFile(params[0], params[1]))
    elif instruction == "fromfile":
        hashmap = HashMap.FromFile(params[0])
    else:
        print("Invalid Instruction")

def ParseInstruction(string):
    sSplit = string.split(" ")
    nums = "0123456789"
    multiplier = string.split("*")
    if len(multiplier) == 1:
        multiplier = 1
    else:
        multiplier = onlyDigits(multiplier[1].split(" ")[0])
        
    for i in range(int(multiplier)):
        if len(sSplit) > 1:
            key = sSplit[1]
            if not key.find("*") == -1:
                key = key[:key.find("*")]
      
            value = " ".join(sSplit[2:])
            RunInstruction(sSplit[0].lower(), (key, value))
        else:
            RunInstruction(sSplit[0].lower(), None)

print("-Instructions-\nAdd [Key] [Value]\nFind [Key]\nRemove [Key]\nClear\nKeys\nValues\nToFile [Path] [Name]\nFromFile [File]\n\n-DEBUG-\nPosition [Key]\nHash [Key]\nPrint")

while True:
    # Newline
    print()
    
    ParseInstruction(input())
