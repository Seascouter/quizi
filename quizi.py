import structures

currentSet = structures.Set("",[])

def loadSet(setName):
    global currentSet
    newSet = structures.Set("",[])
    with open(f"sets/{setName}.set") as f:
        for line in f:
            if line[0] != "{":
                newSet.name = line.strip()
                continue
            line = line.strip()
            line = line[1:-1]
            line = line.split(":")
            for item in range(len(line)):
                line[item] = line[item][1:-1]
            newCard = structures.Card(line[0], line[1])
            newSet.contents.append(newCard)
    currentSet = newSet

def unloadSet():
    global currentSet
    currentSet = structures.Set("",[])
