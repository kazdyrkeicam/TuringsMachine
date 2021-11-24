import re
import string

with open("test3.txt") as file:
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

# pierwsze (dlugosc alfabetu) elementy naleza do pierwszego stanu
# i tak razy ilosc stanow - 1 (bo stan koncowy)

stateNum = len(fileCommand["stany"]) - 1
alphNum = len(fileCommand["alfabet"])

for i in range( stateNum ):
    machineCommand.setdefault(str(i), [])
    for j in range( alphNum ):
        machineCommand[str(i)].append( temp[ (i * alphNum) + j ] )


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


# MAIN #

'''
    fileCommand Construction :
    name : value
'''

'''
    machineCommand :
    state : [ 'SYMBOL;STATE,NEW_SYMBOL,DIRECTION;', '', '' ] -> lists size is the lenght of the alphabet AND this is list of strings
'''

'''
    Call of machineCommand :
    [ STATE ] [ String ] [ Element ]
'''

'''
    What the dog doin?

        while current state is not equal 'k'
            printing the word

            replace the symbol
            choose direction

            change the state
        
        print last state
'''

SYMBOL = 0
STATE = 2
NEW_SYMBOL = 4
DIRECTION = 6

currentState = fileCommand['stan poczatkowy']
word = fileCommand['slowo'] + "_"
head = " "
index = 0

# Dowolna liczba symboli pustych przed jest kasowana
while True:
    if word[index] == "_":
        word = word[1:]
    else:
        break

# Czy zawiera dobre znaki
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

    # Przeciw zapetlanie
    if loopCounter > 100:
        raise ValueError("Przekroczono dopuszczalna liczbe obrotow petli programu!")

print( head + "| stan: " + currentState)
print( "_" + word )

print("procedura zakonczona")