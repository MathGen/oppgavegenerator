
from random import randint
from random import sample
from random import shuffle
from random import choice
import collections
from math import ceil
from oppgavegen.nsp import NumericStringParser
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication, implicit_application,
                                        auto_symbol, implicit_multiplication_application, factorial_notation, convert_xor)
from .models import Template
from django.template.defaultfilters import *
import html
#s = RR(s)
#s = round(s, 3)

#Error message "(╯°□°）╯︵ ┻━┻"
asciimath_sympy_dict = {'int(' : 'integrate('} #for use in converting between sympy and asciimath, might not need this
errorino = "ಠ_ಠ"
errorino2 = "Q_Q"
testerino = "☺☻"

###printer###
#Returns a string
def printer():
    string = "Oppgavegenerator"
    return string

###check_answer###
#Takes both the user answer and answer and checks if they are equal.
#Makes the answers into collections as some questions have multiple answers (ie. x^2 + x + 5).
def checkAnswer(user_answer, answer):
    if collections.Counter(user_answer) == collections.Counter(answer):
        string = "\\text{Du har svart riktig!}"
    else:
        string = "\\text{Du har svart feil. Svaret er: }" + ' og '.join(answer)
    return string

###task_with_solution###
#Makes a valid task with solution from a template in the database.
def task_with_solution(template_id, desired_type='none'):
    error = 0
    if template_id == "":
        q = get_question('algebra')  #gets a question from the DB
    else:
        q = get_question(template_id)
    #I changed this to contain the amount of decimals allowed in the answer, so 0 = False basically.
    #todo make a rounding function using decimals_allowed
    decimals_allowed = int(q.number_of_decimals)
    decimal_allowed = (True if decimals_allowed > 0 else False) #Boolean for if the answer is required to be a integer
    #the domain of random numbers that can be generated for the question
    random_domain_list = (q.random_domain).split('§')
    print(random_domain_list)
    zero_allowed = q.answer_can_be_zero#False #Boolean for 0 being a valid answer or not.
    task = str(q.question_text)
    print(task)
    task = task.replace('\\\\', '\\')
    print(task)
    if desired_type == 'none': # if no type is desired (default), use the type stored in template
        template_type = q.type
    else:
        template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    template_specific = "" #A type specific variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = "" #sends a splitable string since dictionaries can't be passed between layers.
    solution = str(task) + "\n"+str(q.solution).replace('\\\\', '\\') #db automatically adds a extra \ to \ --> \\
    print(solution)
    #solution = solution.replace('\&\#x222B\;', '&#x222B;')
    #todo remove field for template types and just random one of the types for the task, depending on if choices != "" and fill in != ""

    valid_solution = False
    while valid_solution == False: #loop until we get a form of the task that has a valid solution
        variable_dict = generate_valid_numbers(task, random_domain_list, conditions)
        variables_used = dict_to_string(variable_dict) #get a string with the variables used
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
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = calculate_answer(new_choices[x])
        new_choices.append(parse_solution(new_answer).replace('§', 'og'))
        shuffle(new_choices) #Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        template_specific = new_choices
    elif template_type == 'blanks':
        fill_in_dict = fill_in_the_blanks(fill_in)
        new_task = new_task + '\n' + fill_in_dict['fill_in'].replace('\\n', '\n')
        new_task = replace_variables_from_array(variables_used.split('§'), new_task)
        new_task = parse_solution(new_task)
        template_specific = fill_in_dict['hole_positions']
    elif template_type == 'multifill':
        new_choices = choices + '§' + answer.replace('§', 'og')
        template_specific = multifill(new_choices,variable_dict)

    if dictionary is not None:
        new_task = replace_words(new_task, dictionary)
        new_solution = replace_words(new_solution, dictionary) #todo this logic moved into the view. do that.
        #todo might have to send a list of what words were replaced as well (a bit like variables used)
        new_answer = replace_words(new_answer, dictionary)
    number_of_answers = len(new_answer.split('§'))


    #todo also remove parsing of solution in this function as it is not needed before the answer page (only true for normal actually)
    return_dict = {'question' : new_task, 'variable_dictionary' : variables_used, 'template_type' : template_type,
                   'template_specific' : template_specific, 'primary_key' : primary_key, 'number_of_answers' : number_of_answers}
    return return_dict

###validate_solution###
#Checks if the solution made is a valid one according to different tests
#If it isn't a new solution will be made using different values
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

###check_for_decimal###
#Returns True/False depending on if the float has decimals.
#Examples: 5.0000 returns True and 5.12312 returns False
def check_for_decimal(f):
    #todo this might not be necessary or even a good way of doing it
    return float(f).is_integer() #Returns True if f doesn't have a decimal

###calculate_answer###
#Calculates a string using sympify
def calculate_answer(s):
    if not is_number(s):
        s = remove_unnecessary(s)
        s = str(latex_to_sympy(s))
        b = s
        s = s.replace('^', '**')
        if(s[0] == '(') and (s[-1] == ')'):
            s = s[1:len(s)]
        c = s
        s = parse_expr(s, transformations=(convert_xor,standard_transformations, implicit_multiplication_application,),global_dict=None, evaluate=False)
        d = s
        s = latex(sympify(str(s))) #sometimes this returns the value 'zoo' | also could maybe use simplify instead of sympify
    return str(s)

###parse_soltuion###
#Parses a solution (or other string) and calculates using sympify where needed. (between @? ?@)
def parse_solution(solution):
    print('in parse_solution')
    print(solution)
    arr = []
    newArr = []
    recorder = False
    new_solution = solution
    b = ''
    for c in solution:
        if b == '@' and c == '?':
            recorder = True
            s = ''
        elif b == '?' and c == '@':
            recorder = False
            arr.append(s[:-1])
        elif recorder == True:
            s += c
        b=c
    for x in range(len(arr)):
        newArr.append(calculate_answer(str((arr[x]))))
        r = '@?' + arr[x] + '?@'
        new_solution = new_solution.replace(r, newArr[x])
    print(new_solution)
    return new_solution

###get_question###
#Gets a question/template from the database and returns it.
def get_question(topic):
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

###replace_words####
#Replaces variables in a string with the value of a key in the given dictionary.
#Example: "example string: R1", example_dict{'R1', '5'} -> "example string: 5
def replace_words(sentence, dictionary):
    dictionary = dictionary.split('§')
    for i in range(0,len(dictionary)-1,2):
        replace_strings = dictionary[i+1].split(',')
        sentence = sentence.replace(dictionary[i], replace_strings[randint(0,len(replace_strings)-1)])
    return sentence

###calculate_array###
#calculates all the answers in a array
#Example: ['2+2','3+3'] -> [4,6]
def calculate_array(array):
    out_arr = []
    for s in array:
        out_arr.append(calculate_answer(s))
    return out_arr

###after_equal_sign###
#Returns everything after the last = sign of a string
#Example: 'example = string = this' -> ' this'
def after_equal_sign(s):
    if '=' in s:
        s = s.split("=")
        s = s[len(s)-1]
    return s

###replace_variables_from_array###
#Takes a string and replaces variables in the string with ones from the array
#Example: (['R10', '5', 'R1', '7'], 'example string R1 and R10') -> 'example string 7 and 5'
def replace_variables_from_array(arr, s):
    for x in range(0,len(arr)-1,2): #set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s
###parse_answer###
#parses the answer. works for arrays with multiple answers.
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
    #todo change variables to R1R so that R1 won't replace R10, we solve this by doing things backward atm, but that is a bit obtuse.
    hardcoded_variables = ['R22R', 'R21R','R20R','R19R','R18R','R17R','R16R','R15R','R14R','R13R','R12R','R11R','R10R','R9R','R8R','R7R','R6R','R3R','R2R','R1R','R0R']
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
    return variable_dict

###dict to string###
#Returns a seperated string of the key and value pairs of a dict
def dict_to_string(variable_dict):
    variables_used = ""
    for key in variable_dict:
        variables_used += '§' + str(key) + '§' + str(variable_dict[key])
    return variables_used[1:] #Use [1:] to remove unnecessary § from the start

###array_to_string###
#turns a array into a string seperated by §
def array_to_string(array):
    string = ''
    for s in array:
        string += '§' + s
    return string[1:] #Use [1:] to remove unnecessary § from the start

###remove_unnecessary###
#removes unnecessary symbols from a string
def remove_unnecessary(string):
    string = string.replace('@?', '')
    string = string.replace('?@', '')
    return string

### conditions ###
#A function that loops trough the conditions for a given template.
#In the conditions numbers get changed to match the condition. This means all
#Conditions will have to be tried again if one of the conditions fails and changes numbers around.
def check_conditions(conditions, variable_dict,domain_dict):
    redo = True #keeps track of if the conditions have to be tried again
    conditions_dict = {}
    conditions = remove_unnecessary(conditions)

    #Do it the fast way if | and = is not present in conditions
    if (not '|' in conditions) and (not '=' in conditions) and False: #Disabled this for now
        conditions = conditions.split('&')
        while redo:
            counter = 0
            print(conditions)
            for c in conditions:
                print(c)
                if '<' in c:
                    conditions_dict = lesser_than(c, domain_dict, variable_dict)
                elif '>' in c:
                    print(greater_to_lesser_than(c))
                    conditions_dict = lesser_than(greater_to_lesser_than(c), domain_dict, variable_dict)
                variable_dict = conditions_dict['variable_dict'] #Updates the variable dictionary
                something_changed = conditions_dict['something_changed'] #Tells if something has changed
                if something_changed:
                    counter += 1
            if counter == 0:
                redo = False #if nothing has changed, don't try the conditions again
    else: #The slow/random way. todo: find a smart/better way to do this
        #Check conditions --> if false: change a variable -> check conditions
        inserted_conditions = string_replace(conditions, variable_dict)

        while not sympify(latex_to_sympy(inserted_conditions)):
            variable_to_change = choice(list(variable_dict.keys())) #chose a random key from variable_dict
            variable_dict[variable_to_change] = new_random_value(variable_to_change, domain_dict, 0, '')
            inserted_conditions = string_replace(conditions, variable_dict)
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
    while sympify(latex_to_sympy(arr_changed[0] + '<' + arr_changed[1])) == False:
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
#The function also supports a bonus variable which helps in limiting the domain for the variable further if needed.
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
    if string[0] == '(' and string[len(string)-1] == ')':
        string = string[1:len(string)-1]
    string = string.split('>')
    print(string)
    string = string[1] + '<' + string[0]
    print(string)
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

###fill_in_the_blanks###
#Takes the solution and the modified fill_in solution and makes it into a fill in the blanks task.
def fill_in_the_blanks(fill_in):
    hole_dict = find_holes(fill_in)
    max_holes = len(hole_dict)
    number_of_holes = 1
    if max_holes > 1:
        number_of_holes = randint(1,max_holes)
    make_holes_dict = make_holes(hole_dict, fill_in, number_of_holes)
    holes_replaced = make_holes_dict['holes_replaced']

    new_hole_dict = {} #make a dict with only the holes used.
    for s in holes_replaced:
        new_hole_dict[s] = hole_dict[s]
    hole_positions = list(new_hole_dict.values())
    hole_positions = array_to_string(hole_positions)
    fill_in = make_holes_dict['fill_in']
    return_dict = {'fill_in' : fill_in, 'hole_positions' : hole_positions}
    print('hole people hole people..')
    print(hole_positions)
    return return_dict

###find_holes###
#Finds the avaiable holes in the task and their position.
def find_holes(fill_in):
    hole_dict = {} #keeps track of what is getting replaced and the position of that in the string.
    recorder = False
    counter = 0 #keeps track of how far in the string the loop is
    start_point = end_point = 0 #start and end point of box
    a = b = c = d = e = '' #Used to keep track of the last 5 variables iterated over.
    #Note: it might be faster to use a the counter instead of storing previous characters in the for loop.
    for f in fill_in:
        if a == '@' and b == 'x' and c == 'x' and d == 'x' and e == 'x' and f == '@':
            recorder = not(recorder) #flip recorder
            if recorder:
                counter -= 6 #sets the counter back 6 to compensate for @xxxx@ which is not in the original string
                start_point = counter+1
            elif not recorder:
                end_point = counter
                hole_dict[s[:-5]] = str(start_point) + ' ' + str(end_point-5)
                counter -= 6 #sets the counter back 6 to compensate for @xxxx@ which is not in the original string
            s = ''
        elif recorder == True:
            s += f
        counter += 1
        a = b
        b = c
        c = d
        d = e
        e = f
    print(hole_dict)
    return hole_dict

###make_holes###
#Makes holes at random designated places in the solution.
#Returns a dict with the task with holes and also a array of what holes were replaced.
def make_holes(hole_dict, fill_in, number_of_holes):
    possible_holes = list(hole_dict.keys())
    shuffle(possible_holes)
    holes_to_replace = []
    for x in range(number_of_holes):
        holes_to_replace.append(possible_holes[x])
    for s in holes_to_replace:
        fill_in = fill_in.replace('@xxxx@'+s, '\\editable{}'+'@xxxx@')
    fill_in = fill_in.replace('@xxxx@', '')
    return_dict = {'fill_in' : fill_in, 'holes_replaced' : holes_to_replace}
    return return_dict

###get_values_from_position###
#takes a array of positions and returns a array with the strings in between the positional coordinates.
def get_values_from_position(position_string, solution):
    position_array = position_string.split('§')
    values = ''
    for s in position_array:
        positions = s.split()
        values += '§' + (solution[int(positions[0]):int(positions[1])])
    return values[1:]

###multifill###
#Makes the template into a multiple fill in the blanks.
def multifill(choices, variable_dict):
    choices = choices.replace('@?', '')
    choices = choices.replace('?@', '')
    possible_holes = list(variable_dict.keys())
    shuffle(possible_holes)
    choices = choices.split('§')
    shuffle(choices)
    for x in range(len(choices)):
        if choices[x].count(possible_holes[0])>0:
            choices[x]= choices[x].replace(possible_holes[0], '\editable{}')
        else:
            for z in range(1, len(possible_holes)):
                if choices[x].count(possible_holes[z])>0:
                    choices[x]= choices[x].replace(possible_holes[z], '\editable{}')
                    break
    choices = '§'.join(choices)
    choices = string_replace(choices, variable_dict)
    return choices

###template_validation###
#tests a template to see if it makes solvable tasks in a reasonable amount of tries.
def template_validation(template_id):
    valid = False
    template = Template.objects.get(pk=template_id)
    success_string = ""
    counter = 0
    for x in range(0,1000):
        counter += test_template(template_id)
        if counter > 99:
            valid = True
            break
    if valid:
        template.flag = True
        template.save()
        success_string = "Template got through validation!"
    else:
        success_string = "Template failed to be validated."
    return success_string

###Tests_template###
#Tests if the creation of a template ends up with a valid template
def test_template(template_id):
    got_trough_test = 0 #1 if template got through test, and 0 if not.


    return got_trough_test

###latex_to_sympy###
#Turns a string of latex into a string sympy can use.
def latex_to_sympy(expression):
    expression = expression
    expression = expression.replace('{', '(')
    expression = expression.replace('}', ')')
    expression = expression.replace('\\cdot','*')
    expression = expression.replace('\\left','')
    expression = expression.replace('\\right','')
    tempt_expression = ""
    i = 0
    while(i < len(expression)):
        if(expression[i] == '\\'):
            if(expression[i + 1] == 't' and expression[i + 2] == 'e' and expression[i + 3] == 'x' and expression[i + 4] == 't'):
                while(true):
                    if(expression[i] == ')' and counter == 0):
                        break
                    if(expression[i] == '('):
                        counter += 1
                    elif(expression[i+1] == ')'):
                        counter -= 1
                    tempt_expression += expression[i]
                    i += 1
            else:
                while(expression[i] != '(' and expression[i] != ' '):
                    tempt_expression += expression[i]
                    i += 1
        tempt_expression += expression[i]
        i += 1
    expression = tempt_expression

    i = 0
    counter = 0
    recorder = false
    while(i < len(expression)): #logic for insering a / in fractals
        if(expression[i] == 'c' and expression[i-1] == 'a' and expression[i-2] == 'r' and expression[i-3] == 'f' and expression[i-4] == '\\'):
             recorder = true
        if(recorder):
            if(expression[i] == '('):
                counter += 1
            elif(expression[i] == ')'):
                counter -= 1
            if(expression[i] == ')' and counter == 0):
                expression = expression[0:i+1] + "/" + expression[i+1:len(expression)]
                recorder = false
        i+=1
    expression = expression.replace('\\','')
    expression = expression.replace('cdot','*')
    expression = expression.replace('frac','')
    return expression

###is_number###
#Returns wether a string is a number or not.
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False