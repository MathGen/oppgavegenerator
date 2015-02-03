
from random import randint
from random import sample
from math import ceil
from oppgavegen.nsp import NumericStringParser
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication)

def printer():
    string = "Oppgavegenerator"
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
    vh = v+h                              # number of terms (total)
    a = randint(1, 8)                   # term a
    b = randint(1, 8)                   # term b
    c = randint(1, 8)                   # term c
    x = randint(2, 6)                  # given x
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

def algSolution(): #Skriv mer generell løsning der løsningsforslaget brukes som mal
    #decimal = True/False
    oppgave = "r1x = r2 + r3x"
    oppgavetext = "Løs likninga: r1x = r2 + r3x"
    verdier = ['r1', 'r2', 'r3']
    solution = str(oppgave + "\n vi flytter over r3x:\n r1x - r3x = r2\n {r1 - r3}x = r2\n Vi deler på: {r1 - r3}\n x = {r2/(r1-r3)}")
    oppgave2 = "r1 = r2x + r3"
    solution2 = str("\n Vi flytter over r3: \n r1 - r3 = r2x\n {r1 - r3} = r2x \n Vi deler på: r2 \n x = {(r1-r3)/r2}")

    #Av en eller annen grunn splitter python strings med \n character.
    valid_solution = False
    while valid_solution == False:
        new_solution = solution
        new_Oppgave = oppgave
        new_Oppgavetext = oppgavetext
        for i in range(len(verdier)):
            random_tall = str(randint(1,20))
            new_Oppgave = new_Oppgave.replace(verdier[i], random_tall)
           # new_Oppgavetext = new_Oppgavetext.replace(verdier[i], random_tall)
            new_solution = new_solution.replace(verdier[i], random_tall)
        t = standard_transformations + (implicit_multiplication,) #for sikkerhet, gjør om 2x til 2*x
        x = symbols('x')
        #new_Answer = parse_expr(new_Oppgave,  transformations = t)
        new_Answer = new_Oppgave
        s = new_Answer.split('=')
        s[0] = parse_expr(s[0], transformations = t)
        s[1] = parse_expr(s[1], transformations = t)
        new_Answer = solve(Eq(s[0], s[1]), x)
        if new_Answer != []: #Sjekker om new_Answer inneholder svar.
           if new_Answer[0] == ceil(new_Answer[0]): #Sjekker om det er desimaler
                valid_solution = True
    new_solution = parseSolution(new_solution)
    arr = [new_solution, new_Answer[0]]
    return arr

def task_with_solution():
    #I changed this to contain the amount of decimals allowed in the answer, so 0 = False basically.
    decimals_allowed = 1
    decimal_allowed = (True if decimals_allowed > 0 else False) #Boolean for if the answer is required to be a integer
    zero_allowed = False #Boolean for 0 being a valid answer or not.
    task = "r1x = r2 + r3x" #The task
    task_text = "Løs likninga: r1x = r2 + r3x" #the text of the task
    variables = ['r1', 'r2', 'r3'] #The variables used in the task
    solution = str(task + "\n vi flytter over r3x:\n r1x - r3x = r2\n {r1 - r3}x = r2\n Vi deler på: {r1 - r3}\n x = {r2/(r1-r3)}") #Solution for the task
    oppgave2 = "r1 = r2x + r3"
    solution2 = str("\n Vi flytter over r3: \n r1 - r3 = r2x\n {r1 - r3} = r2x \n Vi deler på: r2 \n x = {(r1-r3)/r2}")
    task3 = "integrate(r1*x*sin(r2*x) dx" #husk pluss C
    solution_task3 = str(task3 + "\n Bruker delvis integrasjon: \n integral(uv') dx = uv - integral(u'v) dx) \n setter: u = r1*x og v' = sin(r2*x) \n"
                                 + "da blir: u' = r1 og v = -1/r2 cos(r2*x \n integrate(r1*x*sin(r2*x) dx = \n -(r1*x)/r2*cos(r2*x) - integrate(-1/r2*cos(r2*x))dx = \n"
                                 + "-(r1*x)/r2*cos(r2*x) + 1/r2*integrate(cos(r2*x)) dx =\n {-(r1*x/r2)*cos(r2*x) + 1/(r2*r2)*sin(r2*x)} + C")
    answer_task3 = 'r1*1(r2*r2)*sin(r2*x)-r1*x/r2*cos(r2*x)'
    valid_solution = False
    while valid_solution == False:
        new_solution = solution #solution
        new_Oppgave = task
        new_Oppgavetext = task_text
        for i in range(len(variables)):
            random_tall = str(randint(1,20))
            new_Oppgave = new_Oppgave.replace(variables[i], random_tall)
           # new_Oppgavetext = new_Oppgavetext.replace(verdier[i], random_tall)
            new_solution = new_solution.replace(variables[i], random_tall)
        new_Answer = getAnswerFromSolution(new_solution)
        if new_Answer == 'zoo': #error handling at its finest.
            continue
        valid_solution = validateSolution(new_Answer, decimal_allowed,zero_allowed)
        if  '/' not in str(new_Answer) and 'cos' not in str(new_Answer) and 'sin' not in str(new_Answer) and 'tan' not in str(new_Answer):
            if ((decimal_allowed == False and valid_solution == True) or (checkForDecimal(new_Answer))): #Remove float status if the number is supposed to be a integer
                print("answer is not a float") #todo find out if i need this anymore
                new_Answer = str(int(new_Answer))

    new_solution = parseSolution(new_solution)
    arr = [new_solution, new_Answer]
    return arr
def validateSolution(answer, decimal_allowed, zero_allowed):

    if  '/' not in str(answer) and 'cos' not in str(answer) and 'sin' not in str(answer) and 'tan' not in str(answer):
        print('wtf: ' + str(answer))
        decimal_answer = checkForDecimal(answer)
    elif '/' in str(answer): #checks if the answer contains /.
        decimal_answer = False #technically the answer doesn't contain decimal numbers if for instance it is given on the form 1/5
    else:
        decimal_answer = True
    contains_zero = answer == 0
    valid_solution = True
    if decimal_answer == True and decimal_allowed == False:
        valid_solution = False
    if contains_zero == True and zero_allowed == False:
        valid_solution = False
    return valid_solution
def checkForDecimal(f):
    return float(f).is_integer() #Returns false if f doesn't have a decimal
def getAnswerFromSolution(s): #this function might not be usefull if we implement a answer for every question since we wouldn't have to find the answer then
    answer = ''
    record = False
    for c in s[::-1]:
        if c == '}':
            record = True
        elif c == '{':
            return calculateAnswer(answer)
        elif record == True:
            answer = c + answer
    return s #Returns the original string if there are no calculations, this could be bad though since it would return the whole solution, and not just the answer
def calculateAnswer(s):
    s = sympify(s) #sometimes this returns the value 'zoo' | also could maybe use simplify instead of sympify
    #s = RR(s)
    #s = round(s, 3)
    print(str(s))
    return str(s)
def parseSolution(solution):
    arr = []
    nsp = NumericStringParser()
    newArr = []
    opptak = False
    new_solution = solution
    for c in solution:
        if c == '{':
            opptak = True
            s = ''
        elif c == '}':
            opptak = False
            arr.append(s)
        elif opptak == True:
            s += c
    for x in range(len(arr)):
        newArr.append(calculateAnswer(str((arr[x]))))
        #print(newArr[x])
        r = '{' + arr[x] + '}'
        new_solution = new_solution.replace(r, newArr[x])
    return new_solution
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