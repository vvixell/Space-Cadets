class var:
    def __init__(self, idendifier, value):
        self.identifier = idendifier
        self.value = value

#global variables
Variables = {} #Dictionary of variables
Stack = [] #The stack is used to keep track of loops, each stack frame contains the line index of the start of a loop and the end of the loop

errorCodes = { 
    -1 : "Variable not initialised",
    -2 : "While loop end not found"}

def PrintError(errorMessage, line):
    print("----------------------")
    print(f"Error line: {line}")
    print(f"Reason: {errorCodes[errorMessage]}")
    print("----------------------")


def variableExists(identifier):
    if(identifier in Variables.keys()): return True
    return False

def seperateInstruction(instruction):
    seperatedInstruction = instruction.replace("\n", "")
    seperatedInstruction = seperatedInstruction.split(" ")
    
    while '' in seperatedInstruction:
        seperatedInstruction.remove('')
    return seperatedInstruction

#All the methods used in the bare bones lang
def _clear(identifier):
    Variables[identifier] = 0

def _incr(identifier):
    if(not variableExists(identifier)):
        return -1
    Variables[identifier] = Variables[identifier] + 1

def _decr(identifier):
    if(not variableExists(identifier)):
        return -1
    Variables[identifier] = Variables[identifier] - 1
    if(Variables[identifier] < 0):
        _clear(identifier)

def _while(statements, lineIndex):   
    # Finding the end of the current while loop

    loopCount = 0
    endSearchPointer = lineIndex + 1
    currentInstruction = seperateInstruction(statements[endSearchPointer])[0]
    while (currentInstruction != "end" or loopCount > 0):
        if(currentInstruction == "while"):
            loopCount += 1
        elif(currentInstruction == "end"):
            loopCount -= 1
        endSearchPointer += 1

        if(endSearchPointer >= len(statements)): 
            PrintError(-2, lineIndex)
            return -1 #Error If couldnt find the end of the loop

        currentInstruction = seperateInstruction(statements[endSearchPointer])[0]

    Stack.append([lineIndex, endSearchPointer])
    
    currentInstruction = seperateInstruction(statements[lineIndex])
    var = currentInstruction[1]
    const = (int)(currentInstruction[3])

    if(Variables[var] == const): #Exiting the loop based on condition
        return Stack.pop()[1]+1
    else:
        return lineIndex + 1
    
#end function returns the current line to the start of its corresponding while loop
def _end():
    return Stack.pop()[0] 


def executeLine(statements, lineIndex):
    args = seperateInstruction(statements[lineIndex])
    instruction = args[0]
    match instruction:
        case "clear":
            _clear(args[1])
        case "incr":
            if(_incr(args[1]) == -1):
                PrintError(-1, lineIndex)
                return -1
        case "decr":
            if(_decr(args[1]) == -1):
                PrintError(-1, lineIndex)
                return -1
        case "while":
            return _while(statements, lineIndex)
        case "end":
            return _end()
    return lineIndex + 1

def printVariables(StepCount, currentLine):
    print(f"- Step {StepCount}, CurrentLine {currentLine}-")
    for var in Variables:
        print(f"{var}, {Variables[var]}")

def run():
    FilePath = input("Enter complete file path: \n")
    file = open(FilePath)
    statements = file.read().split(";")
    statements.pop()
    StepCount = 0

    currentLine = 0
    while (currentLine < len(statements)):
        currentLine = executeLine(statements, currentLine)

        if(currentLine < 0):
            break

        StepCount += 1
        printVariables(StepCount, currentLine)
            


run()