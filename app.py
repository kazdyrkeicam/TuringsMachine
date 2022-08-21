import re, sys

if len(sys.argv) == 1:
    print ("Please give a filename")
    sys.exit()

with open(sys.argv[1] + ".txt") as file:
    lines = file.read()

lines = re.split(': |\n', lines)

index = lines.index("instrukcja:")

# temp contains states and moves
temp = list( lines[index + 1:] )
lines = lines[:index]

dict1 = list(lines[i] for i in range(0, len(lines), 2))
dict2 = list(lines[i] for i in range(1, len(lines), 2))

fileCommand = dict(zip(dict1, dict2))

fileCommand["stany"] = fileCommand["stany"].split(",")
fileCommand["alfabet"] = fileCommand["alfabet"].split(",")

machineCommand = dict()

for item in temp:
    if len(item) == 2:
        temp.remove(item)


stateNum = len(fileCommand["stany"]) - 1
alphNum = len(fileCommand["alfabet"])

for i in range( stateNum ):
    machineCommand.setdefault(str(i), [])
    for j in range( alphNum ):
        machineCommand[str(i)].append( temp[ (i * alphNum) + j ] )


def replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring
    return s[:index] + newstring + s[index + 1:]


# MAIN #

SYMBOL = 0
STATE = 2
NEW_SYMBOL = 4
DIRECTION = 6

currentState = fileCommand['stan poczatkowy']
word = fileCommand['slowo'] + "_"
head = " "
index = 0

while True:
    if word[index] == "_":
        word = word[1:]
    else:
        break

allowed_chars = set(fileCommand["alfabet"])
validationString = word
if not set(validationString).issubset(allowed_chars):
    raise ValueError("bledne znaki w slowie")

loopCounter = 0

while currentState != "k":
    print( head + "| stan: " + currentState)
    print( "_" + word )
    
    position = len(head) - 1

    if word[ position ] == "_":
        index = -1
    else:
        index = int( word[ position ] )

    temp = machineCommand[currentState][index]
    word = replacer(word, temp[NEW_SYMBOL], position)
    
    if temp[DIRECTION] == "r":
        head += " "
    elif temp[DIRECTION] == "l":
        head = head[1:]
    
    currentState = temp[STATE]

    loopCounter += 1

    if loopCounter > 100:
        raise ValueError("Przekroczono dopuszczalna liczbe obrotow petli programu!")

print( head + "| stan: " + currentState)
print( "_" + word )

print("procedura zakonczona")