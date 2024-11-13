# AXM
AXM Interpreter

AXM is a simple "assembly like" interpreter written in python, I have plans on converting to c++ at a later date but currently it is just a proof of concept.
Currently it is really hard to work with since it is inspired by Assembly but dumbed down.
AXM can also be slow depenfing on your usecase, as i previously stated, I have plans on converting it to c++ which will imrpove performance

Now for a "tutorial"

To even get started you need to allocate registrey, this can be increased at any time during the program aswell. To allocate memory we use "allocReg", allocReg adds to the size so if you do it with 10 and then 5 the registrey size will become 15.
```
allocReg 10
```
Currently AXM supports 3 datatypes, these are strings, ints and arrays. Arrays can contain any data type. To be able to for example print anything we need to store the data in the registrey, to do this we use "make".
```
make [data] [INDEX]
```
Make string:
```
make "Hello World" 0
```
Make int:
```
make 0 0
```
Make array(Remember, no spaces between the commas):
```
make [0,0] 0
```
printing data:
```
out [REGINDEX]
```

To append to an array we use "append", example:
```
allocReg 1
make [0,0] 0
```

To acces an arrays data we use "->" like this:
```
out [REGINDEX]->[ARRAYINDEX]
```


Functions:

To create a function we use the "fn" keyword along with an "end", everything between fn and end will be the function.
Example:
```
fn Test
make "This is a function call" 0
out 0
end

call Test
```

To call a function we just use the "call" keyword along with the function name:
```
call [NAME]
```

Userinput:
```
get [REGINDEX]
```
This will prompt a user to input data and put it into the index you specify

While is the same as functions, everything between "we" and "end" will be counted as the while loop
Example:
```
make 0 0
make 0 1
we 0 0
out o
end
```

AXM also has a "while not" which works the same as "while2 but instead of "we" we use "wne"

Removeing data from the registrey is simple, we use the keyword "purge", example:
```
purge [REGINDEX]
```

JMP skips past the specified amount of lines. Example:
```
jmp [LINETOSKIP]
```

Jump If, this is a simple command that jumps past the specified amount of lines if 2 registreies are the same. Example
```
ji 0 1 2
```
The previous example checks if reg 0 is the same as reg 1 and if they are skips forward 2 lines.

Jump if not is the exact same but with the keyword "jin"

and ofcourse to prematureley exit the script we use "exit"


Keep in mind that this is a work in progress and is currently very rough with bad error handeling. Please report any bugs or problems that may occur. Also I will convert this to c++ but even then it is a tricky language to work with
