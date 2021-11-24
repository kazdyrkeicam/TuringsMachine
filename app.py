import re
import string

with open("test.txt") as file:
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

WHAT = 0
STATE = 2
ON_WHAT = 4
DIRECTION = 6

currentState = fileCommand['stan poczatkowy']
word = fileCommand['slowo'] + "_"
position = " "
index = 0

for i in range(len(word)):
    if word[ len(position) - 1 ] == "_":
        print( word[-1] )
        index = -1
    else:
        print( int(word[ len(position) - 1 ]) )
        index = int(word[ len(position) - 1 ])

    position += " "

    print( machineCommand[currentState][ index ] )