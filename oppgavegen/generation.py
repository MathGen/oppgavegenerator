
from random import randint
from random import uniform
from random import shuffle
from random import choice
import re
import collections
from math import ceil
from oppgavegen.nsp import NumericStringParser
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication, implicit_application,
                                        auto_symbol, implicit_multiplication_application, factorial_notation, convert_xor)
from .models import Template
from django.contrib.auth.models import User
from django.template.defaultfilters import *
import html

# Error message "(╯°□°）╯︵ ┻━┻"

def check_answer(user_answer, answer):
    """Checks if the answer the user gave is correct.

    :param user_answer: A list containing the answer(s) the user gave
    :param answer: A list containing the answer(s) to the template
    :return: Boolean of whether the answer is 
    """
    for s in answer:
        for us in user_answer:
            if parse_expr(latex_to_sympy(s) + '==' + latex_to_sympy(us), transformations=standard_transformations+(convert_xor, implicit_multiplication_application,),global_dict=None, evaluate=True):
                user_answer.remove(us)
                break

    print(user_answer)
    #if collections.Counter(user_answer) == collections.Counter(answer):
    if user_answer == []:
        right_answer = True
    else:
        right_answer = False
    return right_answer


def generate_task(user, template_id, desired_type='normal'):
    """Makes a valid math question at the correct rating from a template in the database.

    :param user: The user requesting a template
    :param template_id: (optional) A id used for requesting a specific template.
    :param desired_type: (optional) A string for requesting a specific template type.
    :return: Returns a complete math question with generated numbers.
    """
    if template_id == "":
        q = get_question(user, '')  #gets a question from the DB
    else:
        q = get_question(user, template_id)

    if desired_type != 'normal':
        if (desired_type == 'multiple' or desired_type == 'multifill') and not q.multiple_support:
            return  {'question' : 'error'}
        if desired_type == 'blanks' and not q.fill_in:
            return  {'question' : 'error'}

    #the domain of random numbers that can be generated for the question
    random_domain_list = (q.random_domain).split('§')
    task = str(q.question_text)
    task = task.replace('\\\\', '\\')
    template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    template_specific = "" #A type specific variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = "" #sends a splitable string since dictionaries can't be passed between layers. (could serialize instead)
    replacing_words = '' #The words that got replaced, and the words that replaced them

    valid_solution = False
    while valid_solution == False: #loop until we get a form of the task that has a valid solution
        variable_dict = generate_valid_numbers(task, random_domain_list, conditions, False)
        variables_used = dict_to_string(variable_dict) #get a string with the variables used
        new_task = string_replace(task, variable_dict)
        new_answer = string_replace(answer, variable_dict)
        new_choices = string_replace(choices, variable_dict)

        if new_answer == 'error': #error handling at its finest.
            continue #maybe add a counter everytime this happens so that it doesn't loop infinitely for bad templates
        valid_solution = True

    if template_type.lower() == 'multiple':
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = calculate_answer(new_choices[x], q.random_domain)
        new_choices.append(parse_solution(new_answer, q.random_domain).replace('§', 'og'))
        shuffle(new_choices) #Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        template_specific = new_choices
    elif template_type == 'blanks':
        fill_in_dict = fill_in_the_blanks(fill_in)
        new_task = new_task + '\n' + fill_in_dict['fill_in'].replace('\\n', '\n')
        new_task = replace_variables_from_array(variables_used.split('§'), new_task)
        new_task = parse_solution(new_task, q.random_domain)
        template_specific = fill_in_dict['hole_positions']
    elif template_type == 'multifill':
        new_choices = choices + '§' + answer.replace('§', 'og')
        template_specific = multifill(new_choices,variable_dict)

    if dictionary is not None:
        replace_words_dict = replace_words(new_task, dictionary)
        new_task = replace_words_dict['sentence']
        replacing_words = replace_words_dict['replace_string']
    number_of_answers = len(new_answer.split('§'))

    new_task = new_task.replace('+-', '-')
    new_task = new_task.replace('--', '+')
    new_task = parse_solution(new_task, q.random_domain)
    return_dict = {'question' : new_task, 'variable_dictionary' : variables_used, 'template_type' : template_type,
                   'template_specific' : template_specific, 'primary_key' : primary_key,
                   'number_of_answers' : number_of_answers, 'replacing_words' : replacing_words}
    return return_dict


def calculate_answer(s, domain):
    """Calculates a string using sympy.

    :param s: String to be calculated
    :param domain: The domain of the variables.
    :return: A latex version of the calculated string.
    """
    if not is_number(s): #small optimization
        s = remove_unnecessary(s)
        s = str(latex_to_sympy(s))
        s = parse_expr(s, transformations=standard_transformations+(convert_xor, implicit_multiplication_application,),global_dict=None, evaluate=False)
        s = latex(sympify(str(s))) #sometimes this returns the value 'zoo' | also could maybe use simplify instead of sympify
    if is_number(s):
        s = round_answer(domain, float(s))

    return str(s)


def parse_solution(solution, domain):
    """Parses a solution (or other similar string) and calculates where needed. (between @? ?@)

    :param solution: The string to be parsed.
    :param domain: The domain of the different variables.
    :return: A parsed version of the input string (solution)
    """
    #print('in parse_solution')
    #print(solution)
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
        newArr.append(calculate_answer(str((arr[x])), domain))
        r = '@?' + arr[x] + '?@'
        new_solution = new_solution.replace(r, newArr[x])
    print(new_solution)
    return new_solution


def get_question(user, template_id, topic=''):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 40
    increase = 15
    q = ''
    if template_id == '':
        u = User.objects.get(username=user.username)
        user_rating = u.extendeduser.rating
        while True:
            q = Template.objects.filter(rating__gt=(user_rating-slack))
            q = q.filter(rating__lt=(user_rating+slack))
            q = q.filter(valid_flag=True)
            if topic != '':
                q = q.filter(topic_iexact=topic)
            if q:
                q = q[randint(0,q.count()-1)]
                break
            slack += increase
            if slack >= 500:
                q = Template.objects.all()
                q = q.latest('id')
                break
    else:
        q = Template.objects.get(pk=template_id)

    return q


def replace_words(sentence, dictionary):
    """Replaces variables in a string with the value of a key in the given dictionary.
    Example: ('example sentence', 'example § apple, grape') ->
             {'sentence': 'apple sentence', 'replace_string' 'example § apple'}}
    :param sentence: String to replace words in.
    :param dictionary: A splitable (§) string with word alternatives.
    :return: dictionary with the new sentence and a splitable string with what words were replaced
    """
    dictionary = dictionary.split('§')
    replace_string = ''
    for i in range(0,len(dictionary)-1,2):
        replace_strings = dictionary[i+1].split(',')
        replace_word = replace_strings[randint(0,len(replace_strings)-1)]
        sentence = sentence.replace(dictionary[i], replace_word)
        replace_string += '§' + dictionary[i] + '§' + replace_word
    return {'sentence' : sentence, 'replace_string' : replace_string[1:]}


def calculate_array(array, domain):
    """Calculates all the answers in a list.

    Example: ['2+2','3+3'] -> [4,6]
    :param array: List of things to calculate.
    :param domain: Domain for variables.
    :return: Calculated list.
    """
    out_arr = []
    for s in array:
        out_arr.append(calculate_answer(s, domain))
    return out_arr


def after_equal_sign(s):
    """Returns everything after the last '=' sign of a string."""
    if '=' in s:
        s = s.split("=")
        s = s[len(s)-1]
    return s


def replace_variables_from_array(arr, s):
    """Takes a string and replaces variables in the string with ones from the array

    #Example: (['R10', '5', 'R1', '7'], 'example string R1 and R10') -> 'example string 7 and 5'
    :param arr: Array of variables
    :param s: String to replace variables in
    :return: String with replaced variables
    """
    for x in range(0,len(arr)-1,2): #set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s


def parse_answer(answer, domain):
    """Parses the answer. works for arrays with multiple answers."""
    answer = answer.split('§')
    counter = 0
    for s in answer:
        answer[counter] = parse_solution(s, domain)
        if answer[counter] == 'zoo':
            answer = ['error'] #This is an array so that join doesn't return e§r§r§o§r
            continue
        counter += 1
    return '§'.join(answer) #join doesn't do anything if the list has 1 element, except converting it to str


def generate_valid_numbers(Template, random_domain_list, conditions, test):
    """Generates valid numbers using each variables random domain.

    Also makes sure all variables follows the given conditions.
    :param template: The template used.
    :param random_domain_list: List of the random domains.
    :param conditions: The conditions the variable have to follow.
    :param test: If true the function returns the domain_dict instead of variable_dict.
    :return: The current generated variables used in the template.
    """
    hardcoded_variables = ['R22R', 'R21R','R20R','R19R','R18R','R17R','R16R','R15R','R14R','R13R','R12R','R11R','R10R','R9R','R8R','R7R','R6R','R3R','R2R','R1R','R0R']
    domain_dict = {}
    variable_dict = {}
    counter = 0
    #Loops through all possible variable names, and generate a random number for it.
    #Adds the variables names and numbers to the 2 dictionaries and the string
    for i in range(len(hardcoded_variables)):
        if Template.count(hardcoded_variables[i]) > 0:
            #todo add support for domain being a list
            try: #in case of index out of bounds it just uses the first element of the array
                random_domain = random_domain_list[counter].split()
            except IndexError:
                #uses the first domain in case one was not provided.
                random_domain = random_domain_list[0].split()
            random_number = str(make_number(random_domain))
            domain_dict[hardcoded_variables[i]] = random_domain
            variable_dict[hardcoded_variables[i]]= random_number
            counter += 1 #counter to iterate through the random domains
    if len(conditions)>1:
        variable_dict = check_conditions(conditions, variable_dict, domain_dict)

    #lesser_than('R0 * 2 < 3', domain_dict, variable_dict) #for testing purposes
    if test:
        return domain_dict
    return variable_dict


def dict_to_string(variable_dict):
    """Returns a seperated string of the key and value pairs of a dict"""
    variables_used = ""
    for key in variable_dict:
        variables_used += '§' + str(key) + '§' + str(variable_dict[key])
    return variables_used[1:] #Use [1:] to remove unnecessary § from the start


def array_to_string(array):
    """Turns a array into a string separated by §."""
    string = ''
    for s in array:
        string += '§' + s
    return string[1:] #Use [1:] to remove unnecessary § from the start


def remove_unnecessary(string):
    """Removes unnecessary symbols from a string and returns the string."""
    string = string.replace('@?', '')
    string = string.replace('?@', '')
    return string


def check_conditions(conditions, variable_dict,domain_dict):
    """A function that checks if the generated variables pass the conditions and generates new ones until they do.

    :param conditions: The conditions of the template.
    :param variable_dict: List of variables.
    :param domain_dict: the domain of the variables.
    :return: List of variables that pass the conditions of the given template.
    """
    conditions = remove_unnecessary(conditions)
    #The slow/random way. todo: find a smart/better way to do this
    #Check conditions --> if false: change a variable -> check conditions
    inserted_conditions = string_replace(conditions, variable_dict)
    while not parse_expr(latex_to_sympy(inserted_conditions), transformations=standard_transformations+ (convert_xor, implicit_multiplication_application,),global_dict=None, evaluate=True):
        variable_to_change = choice(list(variable_dict.keys())) #chose a random key from variable_dict
        variable_dict[variable_to_change] = new_random_value(variable_to_change, domain_dict, 0, '')
        inserted_conditions = string_replace(conditions, variable_dict)
    return variable_dict


def string_replace(string, variable_dict):
    """Replaces variables in a string with numbers from a dict

    :param string: String with variables in it.
    :param variable_dict: a dictionary with variable names as keys and the number to replace them which as values.
    :return: String with numbers instead of variable names.
    """
    print(variable_dict)
    for key in variable_dict:
        string = string.replace(key, str(variable_dict[key]))
    return string


def get_variables_used(string, variable_dict):
    """Returns what variables are used in the given string as a list."""
    used_variables = []
    for key in variable_dict:
        temp_string = string.replace(key, "")
        if temp_string != string:
            used_variables.append(key)
            string = temp_string
    return used_variables


def new_random_value(value, domain_dict, bonus, arg):
    """Creates a new random value for a given variable using its domain.

    :param value: The value to change.
    :param domain_dict: Domain of the variables, decides what range of the variable and number of decimals.
    :param bonus: Used for limiting the domain for the variable further if needed.
    :param arg: argument for different configurations of what approach to use for the new variable
    :return: New value.
    """
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


def fill_in_the_blanks(fill_in):
    """Returns a fill in the blank template and the position of the holes."""
    print('test')
    print(fill_in)
    hole_dict = find_holes(fill_in)
    number_of_holes = len(hole_dict)
    make_holes_dict = make_holes(hole_dict, fill_in, number_of_holes)
    hole_positions = list(hole_dict.keys())
    hole_positions = array_to_string(hole_positions)
    fill_in = make_holes_dict['fill_in']
    return_dict = {'fill_in' : fill_in, 'hole_positions' : hole_positions}
    print(hole_positions)
    print(return_dict)
    return return_dict


def find_holes(fill_in):
    """Finds the available holes in the template and their position."""
    fill_in = fill_in.split('§') #makes fill in into a list.
    fill_in = fill_in[len(fill_in)-1]
    hole_dict = {} #keeps track of what is getting replaced and the position of that in the string.
    recorder = False
    counter = 0 #keeps track of how far in the string the loop is
    start_point = end_point = 0 #start and end point of box
    a = b = c = d = e = '' #Used to keep track of the last 5 variables iterated over.
    #Note: it might be faster/better to use a counter instead of storing previous characters in the for loop.
    #ie. for x in range(0, len(fill_in). See latex_to_sympy for this in action.
    for f in fill_in:
        if a == '@' and b == 'x' and c == 'x' and d == 'x' and e == 'x' and f == '@':
            recorder = not(recorder) #flip recorder
            if recorder:
                counter -= 6 #sets the counter back 6 to compensate for @xxxx@ which is not in the original string
                start_point = counter+1
            elif not recorder:
                end_point = counter
                #swapping
                #hole_dict[s[:-5]] = str(start_point) + ' ' + str(end_point-5)
                hole_dict[str(start_point) + ' ' + str(end_point-5)] = s[:-5]

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


def make_holes(hole_dict, fill_in, number_of_holes):
    """Inserts holes at given places in the template for fill in the blanks

    :param hole_dict: dictionary of the holes to replace.
    :param fill_in: the template.
    :param number_of_holes: number of holes to create.
    :return: dictionary with fill in the blanks template with holes and which holes were replaced.
    """
    holes_to_replace = list(hole_dict.values())
    for s in holes_to_replace:
        fill_in = fill_in.replace('@xxxx@'+s, '\\editable{}'+'@xxxx@') #why do i add @xxxx@?
    fill_in = fill_in.replace('@xxxx@', '')
    return_dict = {'fill_in' : fill_in, 'holes_replaced' : holes_to_replace}
    return return_dict


def get_values_from_position(position_string, solution):
    """Takes a array of positions and returns a array with the strings in between the positional coordinates."""
    position_array = position_string.split('§')
    values = ''
    for s in position_array:
        positions = s.split()
        values += '§' + (solution[int(positions[0]):int(positions[1])])
    return values[1:]


def multifill(choices, variable_dict):
    """Returns choices with fill in the blanks capability"""
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


def template_validation(template_id):
    """tests a template to see if it makes solvable tasks in a reasonable amount of tries. returns a success string"""
    valid = False
    template = Template.objects.get(pk=template_id)
    counter = 0
    q = Template.objects.get(pk=template_id)
    for x in range(0,10000):
        counter += test_template(q)
        if counter > 99:
            valid = True
            break
    if valid:
        template.valid_flag = True
        template.save()
        success_string = "Mal lagret og validert!"
    else:
        template.valid_flag = False
        template.save()
        success_string = "Mal lagret, men kunne ikke valideres. Rediger malen din å prøv på nytt."
    return success_string


def test_template(template):
    """Tests if the creation of a template ends up with a valid template. Returns 1/0 for success/failure."""
    got_trough_test = 0 #1 if template got through test, and 0 if not.
    #make numbers, check condition, check calculations
    random_domain = template.random_domain
    random_domain_list = random_domain.split('§') #efficiency note: might be faster to pass these, instead of getting them from template every time.
    answer = template.answer
    question = template.question_text
    solution = template.solution
    print(question + solution + answer)
    conditions = template.conditions
    conditions = remove_unnecessary(conditions)

    variable_dict = generate_valid_numbers(question, random_domain_list, "", False) #pass no conditions to to just get back the first numbers made.
    print('this:')
    print(variable_dict)
    domain_dict = generate_valid_numbers(question, random_domain_list, "", True) #pass test = True to get domain_dict instead of variable_dict
    inserted_conditions = (conditions, variable_dict)
    if len(conditions) > 1:
        conditions_pass = sympify(latex_to_sympy(inserted_conditions))
    else:
        conditions_pass = True
    if conditions_pass:
        answer = string_replace(answer,variable_dict)
        solution = string_replace(solution,variable_dict)
        try: #todo: there is probably a better way to do this.
            answer = parse_answer(answer, random_domain)
            solution = parse_solution(solution, random_domain) # Even if this is unused it still checks if parsing the solution crashes.
            got_trough_test = 1
        except Exception:
            pass
        if answer == 'error':
            got_trough_test = 0
    return got_trough_test


def latex_to_sympy(expression):
    """Takes a latex expression and returns a expression sympy can use"""
    expression = expression.replace('\\ne','!=')
    expression = expression.replace('{', '(')
    expression = expression.replace('}', ')')
    expression = expression.replace('\\cdot', '*')
    expression = expression.replace('\\times', '*')
    expression = expression.replace('\\left', '')
    expression = expression.replace('\\right', '')
    expression = expression.replace('∨','|')
    expression = expression.replace('∧','&')
    expression = expression.replace('text( )',' ')
    expression = expression.replace('arcsin','asin')
    expression = expression.replace('arccos','acos')
    expression = expression.replace('arctan','atan')
    expression = expression.replace('arcsec','asec')
    expression = expression.replace('arccosec','acsc')
    expression = expression.replace('arccosec','acsc')
    expression = expression.replace('arccot','acot')
    expression = expression.replace('cosec','csc')
    expression = expression.replace('int','integrate')

    expression = expression.replace('x', ' x')
    expression = expression.replace('y', ' y')
    expression = expression.replace('z', ' z')
    expression = expression.replace('  ', ' ') #remove double whitespace
    expression = expression.replace('ma x (','Max(')
    expression = expression.replace('ma x(','Max(')
    expression = expression.replace('min (','Min(')
    expression = expression.replace('min(','Min(')



    i = 0
    counter = 0
    recorder = false
    while(i < len(expression)): #logic for insering a / in fractals
        if expression[i] == 'c' and expression[i-1] == 'a' and expression[i-2] == 'r' and expression[i-3] == 'f' and expression[i-4] == '\\':
             recorder = true
        if recorder:
            if(expression[i] == '('):
                counter += 1
            elif(expression[i] == ')'):
                counter -= 1
            if(expression[i] == ')' and counter == 0):
                expression = expression[0:i+1] + "/" + expression[i+1:len(expression)]
                recorder = false
        i+=1
    i = 0
    counter = 0
    while i < len(expression): #logic for making \binom(a/b) -> binomial(a,b)
        if expression[i] == 'o' and expression[i-1] == 'n' and expression[i-2] == 'i' and expression[i-3] == 'b' and expression[i-4] == '\\':
             recorder = true
        if recorder:
            if expression[i] == '(':
                counter += 1
            elif expression[i] == ')':
                counter -= 1
            if expression[i] == ')' and counter == 0:
                expression = expression[0:i] + "," + expression[i+2:len(expression)]
                recorder = false
        i+=1
    expression = expression.replace('\\', '')
    expression = expression.replace('frac', '')
    expression = expression.replace('binom', 'binomial')
    return expression


def is_number(s):
    """Returns whether a string is a number or not."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def make_number(domain):
    """Returns a random number within the range and decimal point of the domain given."""
    number = uniform(float(domain[0]), float(domain[1]))
    try:
        number = round(number, int(domain[2]))
        if number.is_integer():
            number = round(number)
    except IndexError:
        number = round(number)
    return number


def round_answer(domain, answer):
    """returns a rounded version of the answer given."""
    answer = float(answer) # Cast it to float. if it is a integer, it will get rounded back to a integer.
    domain = domain.split('§')
    rounding_number = 0
    for s in domain:
        s = s.split()
        try:
            if rounding_number < int(s[2]):
                rounding_number = int(s[2])
        except IndexError:
            pass
    if rounding_number > 0:
        answer = round(answer, rounding_number)
        if answer.is_integer():
            answer = round(answer)
    else:
        answer = round(answer)
    return answer