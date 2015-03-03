
from random import randint
from random import sample
from random import shuffle
import collections
from math import ceil
from oppgavegen.nsp import NumericStringParser
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication)
from .models import Template
from django.template.defaultfilters import *
import html

#new error message "(╯°□°）╯︵ ┻━┻"
errorino = "ಠ_ಠ"
errorino2 = "Q_Q"
testerino = "☺☻"

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
    if collections.Counter(user_answer) == collections.Counter(answer):
        string = "Du har svart riktig!"
    else:
        string = "Du har svart feil. Svaret er: `" + ' og '.join(answer) + '`'
    return string


def algebra(): #Legacy function 
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

def make_variables(amount): #this is not needed anymore
    variables = []
    for x in range(0, amount):
        variables.append('R' + str(x))
    return variables
def task_with_solution():
    error = 0
    q = getQuestion('algebra')  #gets a question from the DB
    #The list is written in reverse to get to the single digit numbers last, as R1 would replace R11-> R19.
    hardcoded_variables = ['R22', 'R21','R20','R19','R18','R17','R16','R15','R14','R13','R12','R11','R10','R9','R8','R7','R6','R3','R2','R1','R0']
    #I changed this to contain the amount of decimals allowed in the answer, so 0 = False basically.
    #todo make a rounding function using decimals_allowed
    decimals_allowed = int(q.number_of_decimals)
    decimal_allowed = (True if decimals_allowed > 0 else False) #Boolean for if the answer is required to be a integer
    random_domain = (q.random_domain).split() #the domain of random numbers that can be generated for the question
    zero_allowed = q.answer_can_be_zero#False #Boolean for 0 being a valid answer or not.
    task = q.question_text
    type = q.type
    choices = q.choices
    dictionary = q.dictionary
    answer = q.answer
    primary_key = q.pk
    variable_dictionary = "" #sends a splitab le string since dictionaries can't be passed between layers.

    solution = str(task) +"\n"+str(q.solution).replace('\\n', '\n') #db automatically adds the escape character \ to strings, so we remove it from \n
    #solution = solution.replace('\&\#x222B\;', '&#x222B;')

    valid_solution = False
    while valid_solution == False: #loop until we get a form of the task that has a valid solution
        new_solution = solution
        new_task = task
        new_answer = answer
        for i in range(len(hardcoded_variables)):
            if new_task.count(hardcoded_variables[i]) > 0:
                random_tall = str(randint(int(random_domain[0]),int(random_domain[1])))
                new_task = new_task.replace(hardcoded_variables[i], random_tall)
                new_solution = new_solution.replace(hardcoded_variables[i], random_tall)
                new_answer = new_answer.replace(hardcoded_variables[i], random_tall)
                variable_dictionary += '§' + hardcoded_variables[i]+ '§' + random_tall #Remove the § later using variable_dictionary[1:]
                if(type.lower() != 'normal'):
                    choices = choices.replace(hardcoded_variables[i], random_tall)
        new_answer = parse_answer(new_answer)

        if new_answer == 'error': #error handling at its finest.
            continue #maybe add a counter everytime this happens so that it doesn't loop infinitely for bad templates
        valid_solution = validate_solution(new_answer, decimal_allowed,zero_allowed)
        if  '/' not in str(new_answer) and 'cos' not in str(new_answer) and 'sin' not in str(new_answer) and 'tan' not in str(new_answer) and '§' not in str(new_answer):
            if ((decimal_allowed == False and valid_solution == True) or (check_for_decimal(new_answer))): #Remove float status if the number is supposed to be a integer
                print("answer is not a float") #todo find out if i need this anymore
                new_answer = str(int(new_answer))
                valid_solution = True

    new_solution = parse_solution(new_solution)
    if type.lower() == 'multiple':
        choices = parse_solution(choices)
        choices = choices.split('§') #if only 1 choice is given it might bug out, we can just enforce 2 choices to be given though..
        choices.append(new_answer)
        shuffle(choices) #Shuffles the choices so that the answer is not always in the same place.
        choices = '§'.join(choices)

    if dictionary is not None:
        new_task = replace_words(new_task, dictionary)
        new_solution = replace_words(new_solution, dictionary)
        new_answer = replace_words(new_answer, dictionary)
        choices = replace_words(choices,dictionary)
    number_of_answers = len(new_answer.split('§'))
    #todo replace new_solution with new_task
    arr = [new_solution, variable_dictionary[1:], type, choices, primary_key, number_of_answers] #Use [1:] to remove unnecessary §
    return arr
def validate_solution(answer, decimal_allowed, zero_allowed):

    if  '/' not in str(answer) and 'cos' not in str(answer) and 'sin' not in str(answer) and 'tan' not in str(answer) and '§' not in str(answer):
        print('(╯°□°）╯︵ ┻━┻: ' + str(answer))
        decimal_answer = check_for_decimal(answer)
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
def check_for_decimal(f):
    return float(f).is_integer() #Returns false if f doesn't have a decimal
def get_answer_from_solution(s): #this function might not be usefull if we implement a answer for every question since we wouldn't have to find the answer then
    answer = ''
    record = False
    b = ""
    for c in s[::-1]:
        if c == '?' and b == '@':
            record = True
        elif c == '@' and b == '?':
            return calculate_answer(answer[1:])
        elif record == True:
            answer = c + answer
        b = c
    return s #Returns the original string if there are no calculations, this could be bad though since it would return the whole solution, and not just the answer
def calculate_answer(s):
    s = sympify(s) #sometimes this returns the value 'zoo' | also could maybe use simplify instead of sympify
    #s = RR(s)
    #s = round(s, 3)
    return str(s)
def parse_solution(solution):
    arr = []
    newArr = []
    opptak = False
    new_solution = solution
    b = ''
    for c in solution:
        if b == '@' and c == '?':
            opptak = True
            s = ''
        elif b == '?' and c == '@':
            opptak = False
            arr.append(s[:-1])
        elif opptak == True:
            s += c
        b=c
    for x in range(len(arr)):
        newArr.append(calculate_answer(str((arr[x]))))
        r = '@?' + arr[x] + '?@'
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

def getQuestion(topic):
    #todo make this general so it doesn't just return a specified result
    q = Template.objects.get(pk=11)
    #q = Template.objects.filter(topic__iexact=topic) #Gets all Templates in that topic
    #q = q.filter(rating ---------)

    #todo add logic for returning 1 random task at appropriate elo.
    #something like SELECT * FROM Template WHERE rating BETWEEN user_rating+- 20
    return q

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '<math>')

def to_asciimath(s): #legacy function, we probably won't need this
    new_s = s
    index = 0
    counter = 0
    #todo: do this only between asciimath delimeters: ``
    for c in s:
        if c == '/' or c == '^':
            new_s = new_s[:index] + c + new_s[index:]
            counter += 1
        index += 1
    return new_s

def replace_words(sentence, dictionary):
    dictionary = dictionary.split('§')
    for i in range(0,len(dictionary)-1,2):
        replace_strings = dictionary[i+1].split(',')
        sentence = sentence.replace(dictionary[i], replace_strings[randint(0,len(replace_strings)-1)])
    return sentence

def calculate_array(array):
    out_arr = []
    for s in array:
        out_arr.append(calculate_answer(s))
    return out_arr

def after_equal_sign(s): #a function that returns everything after the last = sign of the string
    if '=' in s:
        s = s.split("=")
        s = s[len(s)-1]
    return s

def replace_variables_from_array(arr, s): #a function that replaces variables in a string from array
    for x in range(0,len(arr)-1,2): #set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s

def parse_answer(answer):
    answer = answer.split('§')
    counter = 0
    for s in answer:
        answer[counter] = parse_solution(s)
        if answer[counter] == 'zoo':
            answer = ['error'] #This is an array so that join doesn't return e§r§r§o§r
            continue
        counter += 1
    return('§'.join(answer)) #join doesn't do anything if the list has 1 element, except converting it to str