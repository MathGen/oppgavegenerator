
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
def task_with_solution(template_id):
    error = 0
    if template_id == "":
        q = getQuestion('algebra')  #gets a question from the DB
    else:
        q = getQuestion(template_id)
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
    conditions = q.conditions
    dictionary = q.dictionary
    answer = q.answer
    primary_key = q.pk
    variables_used = "" #sends a splitable string since dictionaries can't be passed between layers.
    solution = str(task) +"\n"+str(q.solution).replace('\\n', '\n') #db automatically adds the escape character \ to strings, so we remove it from \n
    #solution = solution.replace('\&\#x222B\;', '&#x222B;')
    #todo remove field for template types and just random one of the types for the task, depending on if choices != "" and fill in != ""

    valid_solution = False
    while valid_solution == False: #loop until we get a form of the task that has a valid solution
        random_replacement_array = generate_valid_numbers(task, random_domain_list, conditions)
        variables_used = random_replacement_array[0]
        variable_dict = random_replacement_array[1]
        new_task = string_replace(task,variable_dict)
        new_answer = string_replace(answer,variable_dict)
        new_solution = string_replace(solution,variable_dict)
        new_choices = string_replace(choices,variable_dict)


        if new_answer == 'error': #error handling at its finest.
            continue #maybe add a counter everytime this happens so that it doesn't loop infinitely for bad templates
        valid_solution = validate_solution(new_answer, decimal_allowed,zero_allowed)

        try:
            int(new_answer) #Check if the answer is a number.
            if ((decimal_allowed == False and valid_solution == True) or (check_for_decimal(new_answer))): #Remove float status if the number is supposed to be a integer
                print("answer is not a float") #todo find out if i need this anymore
                new_answer = str(int(new_answer))
                valid_solution = True
        except: #hardcore error handling
            pass

    new_solution = parse_solution(new_solution)
    if template_type.lower() == 'multiple':
        new_choices = parse_solution(new_choices)
        new_choices = new_choices.split('§') #if only 1 choice is given it might bug out, we can just enforce 2 choices to be given though..
        new_choices.append(new_answer)
        shuffle(new_choices) #Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)

    if dictionary is not None:
        new_task = replace_words(new_task, dictionary)
        new_solution = replace_words(new_solution, dictionary)
        new_answer = replace_words(new_answer, dictionary)
        new_choices = replace_words(new_choices,dictionary)
    number_of_answers = len(new_answer.split('§'))
    if template_type == 'blanks':
        new_task = new_solution
    #todo replace new_solution with new_task
    #todo also remove parsing of solution in this function as it is not needed before the answer page (only true for normal actually)
    arr = [new_task, variables_used, template_type, new_choices, primary_key, number_of_answers] #Use [1:] to remove unnecessary §
    return arr
def validate_solution(answer, decimal_allowed, zero_allowed):

    if  '/' not in str(answer) and 'cos' not in str(answer) and 'sin' not in str(answer) and 'tan' not in str(answer) and '§' not in str(answer):
        print('inside validate solution: ' + str(answer))
        decimal_answer = False #check_for_decimal(parse_answer(answer).replace('`', ''))
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

def getQuestion(topic):
    #todo make this general so it doesn't just return a specified result
    if topic == 'algebra':
        q = Template.objects.all()
        q = q.latest('id')
    else:
        q= Template.objects.get(pk=topic)
    #q = Template.objects.get(pk=7)


    #q = Template.objects.filter(topic__iexact=topic) #Gets all Templates in that topic
    #q = q.filter(rating ---------)

    #todo add logic for returning 1 random task at appropriate elo.
    #something like SELECT * FROM Template WHERE rating BETWEEN user_rating+- 20
    return q


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
###generate_valid_numbers###
#generates valid numbers using each variables random domain.
#also makes sure all variables followes the given conditions.
def generate_valid_numbers(task, random_domain_list, conditions):
    hardcoded_variables = ['R22', 'R21','R20','R19','R18','R17','R16','R15','R14','R13','R12','R11','R10','R9','R8','R7','R6','R3','R2','R1','R0']
    variables_used = ""
    domain_dict = {}
    variable_dict = {}
    counter = 0
    #Loops through all possible variable names, and generate a random number for it.
    #Adds the variables names and numbers to the 2 dictionaries and the string
    for i in range(len(hardcoded_variables)):
        if task.count(hardcoded_variables[i]) > 0:
            #todo add support for domain being a list
            try: #in case of index out of bounds it just uses the first element of the array
                random_domain = random_domain_list[counter].split()
            except IndexError:
                #uses the first domain in case one was not provided.
                random_domain = random_domain_list[0].split()
            random_number = str(randint(int(random_domain[0]),int(random_domain[1])))
            variables_used += '§' + hardcoded_variables[i]+ '§' + random_number #Remove the § later using variable_dictionary[1:]
            domain_dict[hardcoded_variables[i]] = random_domain
            variable_dict[hardcoded_variables[i]]= random_number
            counter += 1 #counter to iterate through the random domains
    if len(conditions)>1:
        variable_dict = check_conditions(conditions, variable_dict, domain_dict)

    #lesser_than('R0 * 2 < 3', domain_dict, variable_dict) #for testing purposes
    return_arr = [variables_used[1:],variable_dict] #Use [1:] to remove unnecessary § from variable_dictionary
    return return_arr

### conditions ###
#A function that loops trough the conditions for a given template.
#In the conditions numbers get changed to match the condition. This means all
#Conditions will have to be tried again if one of the conditions fails and changes numbers around.
def check_conditions(conditions, variable_dict,domain_dict):
    redo = True #keeps track of if the conditions have to be tried again
    conditions = conditions.split('§')
    conditions_dict = {}

    while redo:
        counter = 0
        for c in conditions:
            if '<' in c:
                conditions_dict = lesser_than(c, domain_dict, variable_dict)
            elif '>' in c:
                conditions_dict = lesser_than(greater_to_lesser_than(c), domain_dict, variable_dict)
            variable_dict = conditions_dict['variable_dict'] #Updates the variable dictionary
            something_changed = conditions_dict['something_changed'] #Tells if something has changed
            if something_changed:
                counter += 1
        if counter == 0:
            redo = False #if nothing has changed, don't try the conditions again

    return variable_dict #maybe send a counter with how long it took to get trough conditions

###lesser_than###
#Checks if a lesser_than condition string is true or false.
#If false the values in the string will be replaced and a variable notes that something has changed.
#The function returns a updated dictionary of the variables that are used and also if something has changed
def lesser_than(string, domain_dict, variable_dict):
    #todo i might not have to split arr_changed
    #will loop the full duration if string with no variable is passed. ie. 2 > 4
    counter = 0 #To stop it from looping forever
    something_changed = False #One of the returns values. Shows if something had to be changed.
    arr_changed = string_replace(string, variable_dict).split('<')
    arr_unchanged = string.split('<')
    variables_left = get_variables_used(arr_unchanged[0], variable_dict)
    variables_right = get_variables_used(arr_unchanged[1], variable_dict)
    while sympify(arr_changed[0] + '<' + arr_changed[1]) == False:
        something_changed = True
        change = randint(0,1)
        if (len(variables_right) < 1) and (len(variables_left) < 1):
            print('no variables given') #this is a error where no variables were given ie. 2 > 4
        elif(len(variables_right) < 1):
            change = 0
        elif(len(variables_left) < 1):
            change = 1

        if change == 0 and len(variables_left) > 0: #change the left side of <
            #todo add exception for the sympify
            #todo add compatability with float numbers as well (random.uniform(1.2,1.9))
            variable_to_change = variables_left[randint(0,len(variables_left)-1)]
            new_value = new_random_value(variable_to_change,domain_dict, ceil(solve_inequality(string,variable_dict, variable_to_change)),'left') #todo ceil is only really good for templates with integers.
            variable_dict[variable_to_change] = new_value
        elif change == 1 and len(variables_right) > 0: #change the right side of <
            variable_to_change = variables_right[randint(0,len(variables_right)-1)]
            new_value = new_random_value(variable_to_change,domain_dict, ceil(solve_inequality(string,variable_dict, variable_to_change)), 'right') #Can't just move over - elements as this would fuck over / and *
            variable_dict[variable_to_change] = new_value
        arr_changed = string_replace(string, variable_dict).split('<') #change the values with the new one
        counter += 1
        if counter >= 100:
            break
    print("Sucess: " + '<'.join(arr_changed) + "  counter = " + str(counter))
    return_dict = {'variable_dict' : variable_dict, 'something_changed' : something_changed}
    return return_dict

###string_replace###
#Replaces a string with variables (R0, R1..) with numbers from a dict.
#the dictionary holds keys which are the variables, and values which are the numbers
#A typical variable dict might look like this: {'R0' : 10, R2 : 5}
def string_replace(string, variable_dict):
    for key in variable_dict:
        string = string.replace(key, str(variable_dict[key]))
    return string

###get_variables_used###
#Returns which variables are used in a given string
def get_variables_used(string, variable_dict): #gets the variables used in a string and adds them to a array
    used_variables = []
    for key in variable_dict:
        temp_string = string.replace(key, "")
        if temp_string != string:
            used_variables.append(key)
            string = temp_string
    return used_variables

###new_random_value###
#Creates a new random value for a given variable using it's domain.
#The function also suports a bonus variable which helps in limiting the domain for the variable further if needed.
#It also takes a argument for different configurations of what aproach to use for the new variable
def new_random_value(value, domain_dict, bonus, arg):
    domain = domain_dict[value]
    #kinda interesting: if bonus isn't between the domain values, changing the value won't fix the condition.
    #todo use this fact for good. #savetheworld
    bonus = bonus - 1 #this is because we use smaller than and not <=..
    if arg == 'left': #approach to use if on the left side of lesser than (<)
        if int(domain[0]) <= bonus <= int(domain[1]):
            domain[1] = bonus
        new_value = randint(int(domain[0]), int(domain[1]))
    elif arg == 'right':#approach to use if on the right side of lesser than (<)
        if  int(domain[0]) <= bonus <= int(domain[1]):
            domain[0] = bonus
        new_value = randint(int(domain[0]), int(domain[1]))
    else:
        new_value = randint(int(domain[0]), int(domain[1]))

    return new_value

###greater_to_lesser_than###
# changes x > y into y < x
def greater_to_lesser_than(string):
    string = string.split('>')
    string = string[1] + '<' + string[0]
    return string

###solve_inequality###
#solves inequalities with for 1 unknown
#example: R1 + R2 < R3, solve for R1 where R2 = 10 and R3 = 12
#this gets turned into solve_for_this + 10 < 12 -> solve_for_this < 2
#the function then returns 2
def solve_inequality(inequality, variable_dict, solve_for):
    solve_for_this = symbols('solve_for_this')
    variable_dict[solve_for] = solve_for_this
    inequality = string_replace(inequality, variable_dict)
    inequality_answer = str(solve(inequality, solve_for_this, rational=False))
    #remove unnecessary information from the answer ( for instance it might return 3 > solve_for_this
    #we only need 3 so we remove the > and solve_for_this
    inequality_answer = inequality_answer.replace('<', "")
    inequality_answer = inequality_answer.replace('solve_for_this', "")

    return Float(inequality_answer)