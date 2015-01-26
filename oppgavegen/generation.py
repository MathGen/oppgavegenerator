from random import randint
from random import sample
from math import ceil
from oppgavegen.nsp import NumericStringParser
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication)

def printer():
    string = "Spaghetti"
    return string

def arithmetics():
    number1 = randint(0,10)
    number2 = randint(0,10)
    operators = ["+", "-", "*"]
    opNumber = randint(0,2)
    if opNumber == 0:
        answer = number1 + number2
    elif opNumber == 1:
        answer = number1 - number2
    else:
        answer = number1 * number2
    string = "Hva er " + str(number1) + " " + operators[opNumber] + " " + str(number2) + "?"
    arr = [string, answer]
    return arr

def checkAnswer(user_answer, answer):
    if user_answer == answer:
       string = "Du har svart riktig!"
    else:
        string = "Du har svart feil. Svaret er: " + str(answer)

    return string

def algebra():
    # ax + b = c
    # ax + b = cx
    # ax + bx = c
    # a + bx = c
    # a + b = cx
    # a + bx = cx
    # a + b = c + dx

    v = randint(1, 2)                   # number of terms (left)
    h = randint(1, 2)                   # number of terms (right)
    vh = v+h                            # number of terms (total)
    a = randint(1, 8)                   # term a
    b = randint(1, 8)                   # term b
    c = randint(1, 8)                   # term c
    x = randint(2, 6)                   # given x
    number_of_x = randint(1, vh-1)      # amount of x
    operators = ["+", "-"]
    op_number1 = randint(0, 1)          # first operator
    op_number2 = randint(0, 1)          # second operator
    x_string = [" ", " ", " ", " "]
    x_placement = []
    for i in range(0, vh):
        x_placement += [1]
    if number_of_x == 1:
        i = randint(0, vh-2)
        x_placement[i] = x
        x_string[i] = "x "
    elif number_of_x == 2:
        pos = sample(range(0, vh-1), 2)
        x_placement[pos[0]] = x
        x_placement[pos[1]] = x
        x_string[pos[0]] = "x "
        x_string[pos[1]] = "x "
    else:
        pos = sample(range(0, vh-1), 3)
        x_placement[pos[0]] = x
        x_placement[pos[1]] = x
        x_placement[pos[2]] = x
        x_string[pos[0]] = "x "
        x_string[pos[1]] = "x "
        x_string[pos[2]] = "x "

    ax = a * x_placement[0]
    if vh == 4:
        bx = b * x_placement[1]
        cx = c * x_placement[2]
        if op_number1 == 0 and op_number2 == 0:
            d = (ax + bx - cx) * x_placement[3]
        elif op_number1 == 0 and op_number2 == 1:
            d = (-ax - bx + cx) * x_placement[3]
        elif op_number1 == 1 and op_number2 == 0:
            d = (ax - bx - cx) * x_placement[3]
        else:
            d = (-ax + bx + cx) * x_placement[3]
        string = str(a) + "%s" + str(operators[op_number1]) + " " + str(b) + "%s" + "= " + str(c) + "%s" + str(operators[op_number2]) + " " + str(d) + "%s"
        s = string % (x_string[0], x_string[1], x_string[2], x_string[3])

    if vh == 3:
        bx = b * x_placement[1]
        m = randint(0, 1)
        if m == 0:
            if op_number1 == 0:
                c = (ax + bx) * x_placement[2]
            else:
                c = (ax - bx) * x_placement[2]
            string = str(a) + "%s" + str(operators[op_number1]) + " " + str(b) + "%s" + "= " + str(c) + "%s"
            s = string % (x_string[0], x_string[1], x_string[2])
        else:
            if op_number1 == 0:
                c = (ax - bx) * x_placement[2]
            else:
                c = (-ax + bx) * x_placement[2]
            string = str(a) + "%s" + "= " + str(b) + "%s" + str(operators[op_number1]) + " " + str(c) + "%s"
            s = string % (x_string[0], x_string[1], x_string[2])

    if vh == 2:
        b = ax * x_placement[1]
        string = str(a) + "%s" + "= " + str(b)  + "%s"
        s = string % (x_string[0], x_string[1])

    arr = [s, x]
    return arr

def pypartest():
    string = "4^2"
    nsp = NumericStringParser()
    x=nsp.eval(string)
    s = "hva er " + string + "?"
    arr = [s,int(x)]
    return  arr

def altArithmetics():
    operators = [" + ", " - ", " * "]
    ledd = randint(2,4)
    string = str(randint(0,10)) + operators[randint(0,2)] + str(randint(0,10))
    if ledd > 2:
        for i in range(ledd - 2):
            string+= operators[randint(0,2)] + str(randint(0,10))
    nsp = NumericStringParser()

    x= nsp.eval(string)
    s = "hva er " + string + "?"
    arr = [s,int(x)]
    return arr

def algLosning():
    oppgave = "r1x = r2 + r3x"
    oppgavetext = "Løs likninga: r1x = r2 + r3x"
    verdier = ['r1', 'r2', 'r3']
    losning = str(oppgave + "\n vi flytter over r3x:\n r1x - r3x = r2\n {r1 - r3}x = r2\n Vi deler på: {r1 - r3}\n x = {r2/(r1-r3)}")
    #Av en eller annen grunn splitter python strings med \n character..

    #Replace numbers with random ones
    #check if numbers make sense
    valid_losning = False
    while valid_losning == False:
        nyLosning = losning
        nyOppgave = oppgave
        nyOppgavetext = oppgavetext
        for i in range(len(verdier)):
            random_tall = str(randint(1,20))
            nyOppgave = nyOppgave.replace(verdier[i], random_tall)
           # nyOppgavetext = nyOppgavetext.replace(verdier[i], random_tall)
            nyLosning = nyLosning.replace(verdier[i], random_tall)
        t = standard_transformations + (implicit_multiplication,) #for sikkerhet, gjør om 2x til 2*x
        x = symbols('x')
        #nyttSvar = parse_expr(nyOppgave,  transformations = t)
        nyttSvar = nyOppgave
        s = nyttSvar.split('=')
        s[0] = parse_expr(s[0], transformations = t)
        s[1] = parse_expr(s[1], transformations = t)
        nyttSvar = solve(Eq(s[0], s[1]), x)
        if nyttSvar != []:
           if nyttSvar[0] == ceil(nyttSvar[0]): #Sjekker om det er desimaler
                valid_losning = True
    nyLosning = parseLosning(nyLosning)
    arr = [nyLosning, nyttSvar[0]]
    return arr

def parseLosning(losning):
    arr = []
    nsp = NumericStringParser()
    newArr = []
    opptak = False
    nylosning = losning
    for c in losning:
        if c == '{':
            opptak = True
            s = ''
        elif c == '}':
            opptak = False
            arr.append(s)
        elif opptak == True:
            s += c
    for x in range(len(arr)):
        newArr.append(str(int(nsp.eval(arr[x]))))
        print(newArr[x])
        r = '{' + arr[x] + '}'
        nylosning = nylosning.replace(r, newArr[x])
    return nylosning
def sympyTest():
    t = standard_transformations + (implicit_multiplication,) #for sikkerhet, gjør om 2x til 2*x

    x = symbols('x')
    string = "2x + 4"
    string2 = "8"

    test = parse_expr(string, transformations = t)
    test2 = parse_expr(string2,  transformations = t)
    arr = solve(Eq(test, test2), x)
    out = [string + " = " + string2, arr[0]]

    return out