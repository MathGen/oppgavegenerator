
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
asciimath_sympy_dict = {'int(' : 'integrate('} #for use in converting between sympy and asciimath, might not need this
errorino = "ಠ_ಠ"
errorino2 = "Q_Q"
testerino = "☺☻"

def printer():
    string = "Oppgavegenerator"
    return string

def checkAnswer(user_answer, answer):
    if collections.Counter(user_answer) == collections.Counter(answer):
        string = "Du har svart riktig!"
    else:
        string = "Du har svart feil. Svaret er: `" + '` og `'.join(answer) + '`'
    return string


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
    #the domain of random numbers that can be generated for the question
    random_domain_list = (q.random_domain).split('§')
    print(random_domain_list)
    zero_allowed = q.answer_can_be_zero#False #Boolean for 0 being a valid answer or not.
    task = str(q.question_text).replace('\\n', '\n')
    template_type = q.type
    choices = q.choices
    dictionary = q.dictionary
    answer = q.answer
    primary_key = q.pk
    variable_dictionary = "" #sends a splitable string since dictionaries can't be passed between layers.
    solution = str(task) +"\n"+str(q.solution).replace('\\n', '\n') #db automatically adds the escape character \ to strings, so we remove it from \n
    #solution = solution.replace('\&\#x222B\;', '&#x222B;')

    valid_solution = False
    while valid_solution == False: #loop until we get a form of the task that has a valid solution
        random_replacement_array = replace_numbers(task, answer, solution, random_domain_list, template_type, choices)
        new_task = random_replacement_array[0]
        new_answer = parse_answer(random_replacement_array[1])
        new_solution = random_replacement_array[2]
        variable_dictionary = random_replacement_array[3]
        choices = random_replacement_array[4]

        if new_answer == 'error': #error handling at its finest.
            continue #maybe add a counter everytime this happens so that it doesn't loop infinitely for bad templates
        valid_solution = validate_solution(new_answer, decimal_allowed,zero_allowed)

        try:
            int(new_answer) #Check if the answer is a number.
            if ((decimal_allowed == False and valid_solution == True) or (check_for_decimal(new_answer))): #Remove float status if the number is supposed to be a integer
                print("answer is not a float") #todo find out if i need this anymore
                new_answer = str(int(new_answer))
                valid_solution = True
        except:
            pass

    new_solution = parse_solution(new_solution)
    if template_type.lower() == 'multiple':
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
    if template_type == 'blanks':
        new_task = new_solution
    #todo replace new_solution with new_task
    #todo also remove parsing of solution in this function as it is not needed before the answer page
    arr = [new_task, variable_dictionary, template_type, choices, primary_key, number_of_answers] #Use [1:] to remove unnecessary §
    return arr
def validate_solution(answer, decimal_allowed, zero_allowed):

    if  '/' not in str(answer) and 'cos' not in str(answer) and 'sin' not in str(answer) and 'tan' not in str(answer) and '§' not in str(answer):
        print('inside validate solution: ' + str(answer))
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
    q = Template.objects.all()
    q = q.latest('id')
    #q = Template.objects.get(pk=7)


    #q = Template.objects.filter(topic__iexact=topic) #Gets all Templates in that topic
    #q = q.filter(rating ---------)

    #todo add logic for returning 1 random task at appropriate elo.
    #something like SELECT * FROM Template WHERE rating BETWEEN user_rating+- 20
    return q

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

def replace_numbers(task, solution, answer, random_domain_list, template_type,choices):
    hardcoded_variables = ['R22', 'R21','R20','R19','R18','R17','R16','R15','R14','R13','R12','R11','R10','R9','R8','R7','R6','R3','R2','R1','R0']
    variable_dictionary = ""
    domain_dict = {}
    value_dict = {}

    counter = 0
    for i in range(len(hardcoded_variables)):
        if task.count(hardcoded_variables[i]) > 0:
            try: #in case of index out of bounds it just uses the first element of the array
                random_domain = random_domain_list[counter].split()
            except IndexError:
                #uses the first domain in case one was not provided.
                random_domain = random_domain_list[0].split()

            random_number = str(randint(int(random_domain[0]),int(random_domain[1])))
            task = task.replace(hardcoded_variables[i], random_number)
            solution = solution.replace(hardcoded_variables[i], random_number)
            answer = answer.replace(hardcoded_variables[i], random_number)
            #todo create variable_dictionary after the conditions check out from value dict
            variable_dictionary += '§' + hardcoded_variables[i]+ '§' + random_number #Remove the § later using variable_dictionary[1:]
            if template_type.lower() != 'normal': #incase template_type has been capitalized
                choices = choices.replace(hardcoded_variables[i], random_number)
            domain_dict[hardcoded_variables[i]] = random_domain
            value_dict[hardcoded_variables[i]]= random_number
            counter += 1

    #lesser_than('R0 < R1', domain_dict, value_dict)
    return_arr = [task,solution,answer,variable_dictionary[1:],choices] #Use [1:] to remove unnecessary § from variable_dictionary
    #todo add a dict where the variables in the task that are used gets added sp dict = {R22 : 5, R8 : 1}
    return return_arr

### conditions ###
def conditions(string):

    return

def lesser_than(string, domain_dict, variable_dict):
    #string "r1 < r2"
    #variables is maybe a dict with {R22 : 5, R21 : 2..}
    arr_changed = string_replace(string, variable_dict).split('<')

    arr_unchanged = string.split('<')
    variables_left = get_variables_used(arr_unchanged[0], variable_dict)
    variables_right = get_variables_used(arr_unchanged[1], variable_dict)
    #todo Probably sympify
    while sympify(arr_changed[0] + '>' + arr_changed[1]):
        change = randint(0,1)
        #I need to find variables in a string
        if change == 0: #change in arr[0]
            #todo add exception for the sympify
            #todo add compatability with float numbers as well (random.uniform(1.2,1.9))
            new_value = new_random_value(variables_left[randint[0,len(variables_left)-1]],domain_dict, int(sympify(variables_right)))
            variable_dict[variables_left[randint[0,len(variables_left)-1]]] = new_value
        else: #change in arr[1]
            new_value = new_random_value(variables_right[randint[0,len(variables_right)-1]],domain_dict, int(sympify(variables_left)))
            variable_dict[variables_right[randint[0,len(variables_right)-1]]] = new_value
        arr_changed = string_replace(string, variable_dict).split('<')
    print("Sucess: " + '<'.join(arr_changed))
    return

def string_replace(string, variable_dict):
    for key in variable_dict:
        string = string.replace(key, variable_dict[key])
    return string

def get_variables_used(string, variable_dict): #gets the variables used in a string and adds them to a array
    used_variables = []
    for key in variable_dict:
        temp_string = string.replace(key, "")
        if temp_string == string:
            used_variables.append(key)
            string = temp_string
    return used_variables

def new_random_value(value, domain_dict, bonus):
    #value R2
    #todo: Finish this function
    #domain ['2 3', '3 4']
    return