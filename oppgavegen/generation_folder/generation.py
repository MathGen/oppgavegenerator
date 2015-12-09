"""

Handles task generation from templates.

"""

from random import uniform, shuffle, choice
import json

from sympy import sympify

from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

from oppgavegen.parsing.latex_translator import latex_to_sympy
from oppgavegen.view_logic.rating import calculate_and_update_offset
from oppgavegen.models import Level
from oppgavegen.generation_folder.multifill import multifill
from oppgavegen.generation_folder.fill_in import fill_in_the_blanks
from oppgavegen.parsing.parenthesis_removal import *
from oppgavegen.utility.utility import *
from oppgavegen.generation_folder.calculate_parse_solution import parse_solution
from oppgavegen.generation_folder.get_question import get_question, get_level_question


@Debugger
def generate_task(user, template_extra, desired_type=''):
    """Makes a valid math question at the correct rating from a template in the database.

    :param user: The user requesting a template
    :param template_extra: (optional) A id used for requesting a specific template.
    :param desired_type: (optional) A string for requesting a specific template type.
    :return: Returns a complete math question with generated numbers.
    """
    if template_extra == "":
        get_question_dict = get_question(user, '')  # Gets a question from the DB
    else:
        get_question_dict = get_question(user, template_extra)

    q = get_question_dict['template']
    if desired_type == '':
        desired_type = get_question_dict['type']
    if desired_type != 'normal':
        if (desired_type == 'multiple' or desired_type == 'multifill') and not q.multiple_support:
            return {'question': 'error'}
        if desired_type == 'blanks' and not q.fill_in:
            return {'question': 'error'}

    # The domain of random numbers that can be generated for the question
    random_domain_list = q.random_domain
    task = str(q.question_text)
    task = task.replace('\\\\', '\\') # Replaces double \\ with \
    task = task.replace('(', '+parenthesisleft+')  # Done to preserve original parenthesis
    task = task.replace(')', '+parenthesisright+')  # Done to preserve original parenthesis

    template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    choices = choices.replace('(', '+parenthesisleft+')  # Done to preserve original parenthesis
    choices = choices.replace(')', '+parenthesisright+')  # Done to preserve original parenthesis
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    fill_in = fill_in.replace('(', '+parenthesisleft+')  # Done to preserve original parenthesis
    fill_in = fill_in.replace(')', '+parenthesisright+')  # Done to preserve original parenthesis
    template_specific = ""  # A variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = ""  # Sends a splitable string since dictionaries can't be passed between layers.
    replacing_words = ''  # The words that got replaced, and the words that replaced them

    graph = q.graph  # took out .replace('\\\\', '\\')
    if graph:
        graph = json.loads(graph)

    #task = add_phantom_minus(task)
    #answer = add_phantom_minus(answer)
    #choices = add_phantom_minus(choices)
    new_choices = ''
    new_task = ''
    new_answer = ''
    variable_dict = ''

    valid_solution = False
    while valid_solution is False:  # Loop until we get a form of the task that has a valid solution
        variable_dict = generate_valid_numbers(task, random_domain_list, conditions, False)
        variables_used = dict_to_string(variable_dict)  # Get a string with the variables used
        new_task = string_replace(task, variable_dict)
        new_answer = string_replace(answer, variable_dict)
        new_choices = string_replace(choices, variable_dict)

        for x in range(0, len(graph)):
            graph[x] = string_replace(graph[x], variable_dict)
            graph[x] = parse_solution(graph[x], q.random_domain)

        if new_answer == 'error':
            continue  # Retry if the current template resulted in a error.
        valid_solution = True

    if template_type.lower() == 'multiple':
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = parse_solution(new_choices[x], q.random_domain)
        new_choices.append(parse_solution(new_answer, q.random_domain).replace('§', 'og'))
        shuffle(new_choices)  # Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        new_choices = parenthesis_removal(new_choices)
        template_specific = new_choices
        #template_specific = remove_pm_and_add_parenthesis(template_specific)
    elif template_type == 'blanks':
        fill_in_dict = fill_in_the_blanks(fill_in)
        # new_task = new_task + '\n' + fill_in_dict['fill_in'].replace('\\n', '\n')
        new_task = new_task + '§' + fill_in_dict['fill_in']
        new_task = replace_variables_from_array(variables_used.split('§'), new_task)
        new_task = parse_solution(new_task, q.random_domain)
        template_specific = fill_in_dict['hole_positions']
    elif template_type == 'multifill':
        new_choices = choices + '§' + answer.replace('§', 'og')
        new_choices = parenthesis_removal(new_choices)
        template_specific = multifill(new_choices, variable_dict)

    if dictionary is not None:
        replace_words_dict = replace_words(new_task, dictionary)
        new_task = replace_words_dict['sentence']
        replacing_words = replace_words_dict['replace_string']
    number_of_answers = len(new_answer.split('§'))

    if graph != None and graph != '':  # to prevent error if none
        graph = json.dumps(graph)
    new_task = parse_solution(new_task, q.random_domain)
    #new_task = remove_pm_and_add_parenthesis(new_task)
    new_task = parenthesis_removal(new_task)

    return_dict = {'question': new_task,
                   'variable_dictionary': variables_used, 'template_type': template_type,
                   'template_specific': template_specific, 'primary_key': primary_key,
                   'number_of_answers': number_of_answers, 'replacing_words': replacing_words,
                   'graph': graph, 'graph_settings': q.graph_settings, 'graph_color': q.graph_color}
    return return_dict


@Debugger
def generate_level(user, level_id):
    """Makes a valid math question at the correct rating from a template in the database.

    :param user: The user requesting a template
    :param template_extra: (optional) A id used for requesting a specific template.
    :param desired_type: (optional) A string for requesting a specific template type.
    :return: Returns a complete math question with generated numbers.
    """
    level = Level.objects.get(pk=level_id)
    calculate_and_update_offset(level)
    get_question_dict = get_level_question(user, level)  # Gets a template from the DB
    q = get_question_dict['template']
    desired_type = get_question_dict['type']
    # The domain of random numbers that can be generated for the question
    random_domain_list = q.random_domain
    task = str(q.question_text)
    task = task.replace('\\\\', '\\') # Replaces double \\ with \
    task = task.replace('(', '+parenthesisleft+')  # Done to preserve original parenthesis
    task = task.replace(')', '+parenthesisright+')  # Done to preserve original parenthesis
    template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    choices = choices.replace('(', '+parenthesisleft+')
    choices = choices.replace(')', '+parenthesisright+')
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    fill_in = fill_in.replace('(', '+parenthesisleft+')  # Done to preserve original parenthesis
    fill_in = fill_in.replace(')', '+parenthesisright+')  # Done to preserve original parenthesis
    template_specific = ""  # A variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = ""
    replacing_words = ''  # The words that got replaced, and the words that replaced them

    #task = add_phantom_minus(task)
    #answer = add_phantom_minus(answer)
    #choices = add_phantom_minus(choices)

    new_choices = ''
    new_task = ''
    new_answer = ''
    variable_dict = ''
    graph = q.graph  # took out .replace('\\\\', '\\')
    if graph:
        graph = json.loads(graph)

    valid_solution = False
    while valid_solution is False:  # Loop until we get a form of the task that has a valid solution
        variable_dict = generate_valid_numbers(task, random_domain_list, conditions, False)
        variables_used = dict_to_string(variable_dict)  # Get a string with the variables used
        new_task = string_replace(task, variable_dict)
        new_answer = string_replace(answer, variable_dict)
        new_choices = string_replace(choices, variable_dict)

        for x in range(0, len(graph)):
            graph[x] = string_replace(graph[x], variable_dict)
            graph[x] = parse_solution(graph[x], q.random_domain)

        if new_answer == 'error':
            continue  # Retry if the current template resulted in a error.
        valid_solution = True

    if template_type.lower() == 'multiple':
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = parse_solution(new_choices[x], q.random_domain)
        new_choices.append(parse_solution(new_answer, q.random_domain).replace('§', 'og'))
        shuffle(new_choices)  # Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        new_choices = parenthesis_removal(new_choices)
        template_specific = new_choices
        #template_specific = remove_pm_and_add_parenthesis(template_specific)
    elif template_type == 'blanks':
        fill_in_dict = fill_in_the_blanks(fill_in)
        # new_task = new_task + '\n' + fill_in_dict['fill_in'].replace('\\n', '\n')
        new_task = new_task + '§' + fill_in_dict['fill_in']
        new_task = replace_variables_from_array(variables_used.split('§'), new_task)
        new_task = parse_solution(new_task, q.random_domain)
        template_specific = fill_in_dict['hole_positions']
    elif template_type == 'multifill':
        new_choices = choices + '§' + answer.replace('§', 'og')
        template_specific = multifill(new_choices, variable_dict)

    if dictionary is not None:
        replace_words_dict = replace_words(new_task, dictionary)
        new_task = replace_words_dict['sentence']
        replacing_words = replace_words_dict['replace_string']
    number_of_answers = len(new_answer.split('§'))

    if graph != None and graph != '':  # to prevent error if none
        graph = json.dumps(graph)
    new_task = parse_solution(new_task, q.random_domain)
    # new_task = remove_pm_and_add_parenthesis(new_task)

    new_task = parenthesis_removal(new_task)

    return_dict = {'question': new_task, 'variable_dictionary': variables_used, 'template_type': template_type,
                   'template_specific': template_specific, 'primary_key': primary_key,
                   'number_of_answers': number_of_answers, 'replacing_words': replacing_words,
                   'graph': graph, 'graph_settings': q.graph_settings, 'graph_color': q.graph_color}
    return return_dict

@Debugger
def generate_valid_numbers(template, random_domain, conditions, test):
    """Generates valid numbers using each variables random domain.

    Also makes sure all variables follows the given conditions.
    :param template: The template used.
    :param random_domain: dict used for random domains
    :param conditions: The conditions the variable have to follow.
    :param test: If true the function returns the domain_dict instead of variable_dict.
    :return: The current generated variables used in the template.
    """
    hardcoded_variables = ['R22R', 'R21R', 'R20R', 'R19R', 'R18R', 'R17R', 'R16R', 'R15R', 'R14R', 'R13R', 'R12R',
                           'R11R', 'R10R', 'R9R', 'R8R', 'R7R', 'R6R', 'R3R', 'R2R', 'R1R', 'R0R']
    domain_dict = {}
    domain_list = {}
    variable_dict = {}
    try:
        random_domain = json.loads(random_domain)
        # Loops through all possible variable names, and generate a random number for it.
        # Adds the variables names and numbers to the 2 dictionaries and the string
        for key in random_domain:
            if random_domain[key][1]:
                random_number = str(make_number_from_list(random_domain[key][0]))
            else:
                random_number = str(make_number(random_domain[key][0]))
            domain_dict[key] = random_domain[key][0]
            domain_list[key] = random_domain[key][1]
            variable_dict[key] = random_number
    except ValueError:
        pass

    if len(conditions) > 1:
        variable_dict = check_conditions(conditions, variable_dict, domain_dict, domain_list)

    # lesser_than('R0 * 2 < 3', domain_dict, variable_dict) #for testing purposes
    if test:
        return domain_dict
    return variable_dict


@Debugger
def check_conditions(conditions, variable_dict, domain_dict, domain_list):
    """A function that checks if the generated variables pass the conditions and generates new ones until they do.
    :param conditions: The conditions of the template.
    :param variable_dict: List of variables.
    :param domain_dict: the domain of the variables.
    :param domain_list: a dict with the domain list.
    :return: List of variables that pass the conditions of the given template.
    """
    conditions = remove_unnecessary(conditions)
    # Check conditions --> if false: change a variable -> check conditions
    inserted_conditions = string_replace(conditions, variable_dict)
    while not parse_expr(latex_to_sympy(inserted_conditions), transformations=standard_transformations +
                         (convert_xor, implicit_multiplication_application,), global_dict=None, evaluate=True):
        variable_to_change = choice(list(variable_dict.keys()))  # Chose a random key from variable_dict
        if domain_list[variable_to_change]:
            variable_dict[variable_to_change] = make_number_from_list(domain_dict[variable_to_change])
        else:
            variable_dict[variable_to_change] = new_random_value(variable_to_change, domain_dict)
        inserted_conditions = string_replace(conditions, variable_dict)
    return variable_dict


@Debugger
def get_variables_used(string, variable_dict):
    """Returns what variables are used in the given string as a list."""
    used_variables = []
    for key in variable_dict:
        temp_string = string.replace(key, "")
        if temp_string != string:
            used_variables.append(key)
            string = temp_string
    return used_variables


@Debugger
def new_random_value(value, domain_dict, bonus=0, extra=''):
    """Creates a new random value for a given variable using its domain.

    :param value: The value to change.
    :param domain_dict: Domain of the variables, decides what range of the variable and number of decimals.
    :param bonus: Used for limiting the domain for the variable further if needed.
    :param extra: argument for different configurations of what approach to use for the new variable
    :return: New value.
    """
    domain = domain_dict[value]
    # If bonus isn't between the domain values, changing the value won't fix the condition.
    bonus -= 1  # This is because we use smaller than and not <=..
    if extra == 'left':  # Approach to use if on the left side of lesser than (<)
        if int(domain[0]) <= bonus <= int(domain[1]):
            domain[1] = bonus
        new_value = randint(int(domain[0]), int(domain[1]))
    elif extra == 'right':  # Approach to use if on the right side of lesser than (<)
        if int(domain[0]) <= bonus <= int(domain[1]):
            domain[0] = bonus
        new_value = randint(int(domain[0]), int(domain[1]))
    else:
        new_value = randint(int(domain[0]), int(domain[1]))
    return new_value

def make_number_from_list(domain):
    return sympify(latex_to_sympy(choice(domain)))


@Debugger
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

