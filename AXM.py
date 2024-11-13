import sys
import re

def remove_comments(line):
    inside_string = False
    result = []

    for i, char in enumerate(line):
        if char == '"' and (i == 0 or line[i-1] != '\\'):
            inside_string = not inside_string
        if char == "#" and not inside_string:
            break
        result.append(char)

    return ''.join(result).strip()

script = None
if len(sys.argv) <= 1:
    script = open("commandLine.axm", "r").readlines()
else:
    script = open(sys.argv[1], "r").readlines()
script = [remove_comments(line) for line in script]

c = 0
for i in script:
    if "\n" in i:
        script[c] = i[:-1]
    c += 1

functions = []

mainReg = []
sideReg = []

def interpret(insts, Reg):
    a = 0
    while a < len(insts):
        if insts[a] == "":
            a += 1
            continue
        i = insts[a]

        instruction = re.findall(r'".*?"|\S+', i)
        op = instruction[0]
        if op == "allocReg":
            for i in range(int(instruction[1])): #allocReg [RANGE]
                Reg.append(None)
        elif op == "fn": #fn [NAME] -> end
            fName = instruction[1]
            a += 1
            f = []
            while a < len(insts) and insts[a].strip() != "end":
                f.append(insts[a].strip())
                a += 1
            functions.append([fName, f])
        elif op == "make": #make [DATA] [REGPOS]
            if int(instruction[2]) > len(Reg)-1:
                print("ERROR, Out of memory at line: ", str(a+1))
                exit()
            if "[" in instruction[1] and "]" in instruction[1]: #Fix space error
                arr = []
                inDts = instruction[1][:-1][1:].split(",")
                for i in inDts:
                    if '"' in i:
                        arr.append(i[:-1][1:])
                    else:
                        arr.append(int(i))

                Reg[int(instruction[2])] = arr
            elif '"' in instruction[1]:
                Reg[int(instruction[2])] = instruction[1][:-1][1:]
            else:
                Reg[int(instruction[2])] = int(instruction[1])
        elif op == "out": #out [REGPOS]
            if not "->" in instruction[1] and Reg[int(instruction[1])] == None:
                print("ERROR, registrey collumn is empty at line: ", str(a+1))
                exit()
            else:
                d = None
                if "->" in instruction[1]:
                    spl = instruction[1].split("->")
                    d = Reg[int(spl[0])][int(spl[1])]
                    if type(d) == str and "\\n" in d:
                        print(d.replace("\\n", ""))
                    else:
                        print(d, end="")
                else:
                    if type(Reg[int(instruction[1])]) == str and "\\n" in Reg[int(instruction[1])]:
                        print(Reg[int(instruction[1])].replace("\\n", ""))
                    else:
                        print(Reg[int(instruction[1])], end="")
        elif op == "add": #add [DATA1] [DATA2] [REGPOS]
            d1 = None
            d2 = None
            
            if "->" in instruction[1]:
                spl = instruction[1].split("->")
                d1 = Reg[int(spl[0])][int(spl[1])]
            else:
                d1 = Reg[int(instruction[1])]
            if "->" in instruction[2]:
                spl = instruction[2].split("->")
                d2 = Reg[int(spl[0])][int(spl[1])]
            else:
                d2 = Reg[int(instruction[2])]

            Reg[int(instruction[3])] = (int(d1) + int(d2))
        elif op == "sub": #sub [DATA1] [DATA2] [REGPOS]
            d1 = None
            d2 = None
            
            if "->" in instruction[1]:
                spl = instruction[1].split("->")
                d1 = Reg[int(spl[0])][int(spl[1])]
            else:
                d1 = Reg[int(instruction[1])]
            if "->" in instruction[2]:
                spl = instruction[2].split("->")
                d2 = Reg[int(spl[0])][int(spl[1])]
            else:
                d2 = Reg[int(instruction[2])]

            Reg[int(instruction[3])] = (int(d1) - int(d2))
        elif op == "div": #div [DATA1] [DATA2] [REGPOS]
            d1 = None
            d2 = None
            
            if "->" in instruction[1]:
                spl = instruction[1].split("->")
                d1 = Reg[int(spl[0])][int(spl[1])]
            else:
                d1 = Reg[int(instruction[1])]
            if "->" in instruction[2]:
                spl = instruction[2].split("->")
                d2 = Reg[int(spl[0])][int(spl[1])]
            else:
                d2 = Reg[int(instruction[2])]

            Reg[int(instruction[3])] = (int(d1) / int(d2))
        elif op == "mul": #mul [DATA1] [DATA2] [REGPOS]
            d1 = None
            d2 = None
            
            if "->" in instruction[1]:
                spl = instruction[1].split("->")
                d1 = Reg[int(spl[0])][int(spl[1])]
            else:
                d1 = Reg[int(instruction[1])]
            if "->" in instruction[2]:
                spl = instruction[2].split("->")
                d2 = Reg[int(spl[0])][int(spl[1])]
            else:
                d2 = Reg[int(instruction[2])]

            Reg[int(instruction[3])] = (int(d1) * int(d2))
        elif op == "call": #call [FUNCTIONNAME]
            for i in functions:
                if i[0] == instruction[1]:
                    interpret(i[1], Reg)
                    break
        elif op == "purge": #purge [REGPOS]
            Reg[int(instruction[1])] = None
        elif op == "ji": #ji [REG1] [REG2] [LINE]
            if Reg[int(instruction[1])] == Reg[int(instruction[2])]:
                #a = int(instruction[3])-1
                a += int(instruction[3])
                continue
        elif op == "jin": #jin [REG1] [REG2] [LINE]
            if Reg[int(instruction[1])] != Reg[int(instruction[2])]:
                #a = int(instruction[3])-1
                a += int(instruction[3])
                continue
        elif op == "we": #we [REG1] [REG2]. we = while equal
            a += 1
            f = []
            while a < len(insts) and insts[a].strip() != "end":
                f.append(insts[a].strip())
                a += 1
            while Reg[int(instruction[1])] == Reg[int(instruction[2])]:
                interpret(f, Reg)
        elif op == "wne": #we [REG1] [REG2]. wne = while not equal
            a += 1
            f = []
            while a < len(insts) and insts[a].strip() != "end":
                f.append(insts[a].strip())
                a += 1
            while Reg[int(instruction[1])] != Reg[int(instruction[2])]:
                interpret(f, Reg)
        elif op == "jmp": #jmp [LINE]
            #a = int(instruction[1])
            a += int(instruction[1])
        elif op == "get": #get [REG]
            Reg[int(instruction[1])] = input()
        elif op == "append": #append [DATA] [REG]
            if not type(Reg[int(instruction[2])]) == list:
                print("ERROR, tried appending to a none array, at line: " + str(a + 1))
                exit()
            if not '"' in instruction[1]:
                Reg[int(instruction[2])].append(int(instruction[1]))
            else:
                Reg[int(instruction[2])].append(instruction[1][:-1][1:])
        elif op == "exit": #exit
            exit()
        elif op == "interpret":
            f = [Reg[int(instruction[1])]]
            interpret(f, sideReg)
        a += 1

interpret(script, mainReg)
