"""

Handles task generation from templates.

"""

from random import randint, uniform, shuffle, choice
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy
from .models import Template, Level, UserLevelProgress
from django.contrib.auth.models import User
from oppgavegen.decorators import Debugger
from oppgavegen.generation_folder.multifill import multifill
from oppgavegen.generation_folder.fill_in import fill_in_the_blanks
from oppgavegen.generation_folder.utility import replace_words, dict_to_string, string_replace
from oppgavegen.generation_folder.calculate_parse_solution import parse_solution, calculate_answer


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
    elif template_extra.isdigit():
        get_question_dict = get_question(user, template_extra)
    else:
        get_question_dict = get_question(user, '', template_extra)
    q = get_question_dict['template']
    if desired_type == '':
        desired_type = get_question_dict['type']
    if desired_type != 'normal':
        if (desired_type == 'multiple' or desired_type == 'multifill') and not q.multiple_support:
            return {'question': 'error'}
        if desired_type == 'blanks' and not q.fill_in:
            return {'question': 'error'}

    # The domain of random numbers that can be generated for the question
    random_domain_list = q.random_domain.split('§')
    task = str(q.question_text)
    task = task.replace('\\\\', '\\') # Replaces double \\ with \
    template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    template_specific = ""  # A variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = ""  # Sends a splitable string since dictionaries can't be passed between layers.
    replacing_words = ''  # The words that got replaced, and the words that replaced them

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

        if new_answer == 'error':
            continue  # Retry if the current template resulted in a error.
        valid_solution = True

    if template_type.lower() == 'multiple':
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = calculate_answer(new_choices[x], q.random_domain)
        new_choices.append(parse_solution(new_answer, q.random_domain).replace('§', 'og'))
        shuffle(new_choices)  # Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        template_specific = new_choices
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

    new_task = new_task.replace('+-', '-')
    new_task = new_task.replace('--', '+')
    new_task = parse_solution(new_task, q.random_domain)
    return_dict = {'question': new_task, 'variable_dictionary': variables_used, 'template_type': template_type,
                   'template_specific': template_specific, 'primary_key': primary_key,
                   'number_of_answers': number_of_answers, 'replacing_words': replacing_words}
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
    get_question_dict = get_level_question(user, level)  # Gets a template from the DB
    q = get_question_dict['template']
    desired_type = get_question_dict['type']
    # The domain of random numbers that can be generated for the question
    random_domain_list = q.random_domain.split('§')
    task = str(q.question_text)
    task = task.replace('\\\\', '\\') # Replaces double \\ with \
    template_type = desired_type
    choices = q.choices.replace('\\\\', '\\')
    conditions = q.conditions.replace('\\\\', '\\')
    dictionary = q.dictionary
    answer = q.answer.replace('\\\\', '\\')
    primary_key = q.pk
    fill_in = q.fill_in.replace('\\\\', '\\')
    template_specific = ""  # A variable that holds the extra values for a given type. ie. choices for multiple.
    variables_used = ""  # Sends a splitable string since dictionaries can't be passed between layers.
    replacing_words = ''  # The words that got replaced, and the words that replaced them

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

        if new_answer == 'error':
            continue  # Retry if the current template resulted in a error.
        valid_solution = True

    if template_type.lower() == 'multiple':
        new_choices = new_choices.split('§')
        for x in range(len(new_choices)):
            new_choices[x] = calculate_answer(new_choices[x], q.random_domain)
        new_choices.append(parse_solution(new_answer, q.random_domain).replace('§', 'og'))
        shuffle(new_choices)  # Shuffles the choices so that the answer is not always in the same place.
        new_choices = '§'.join(new_choices)
        template_specific = new_choices
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

    new_task = new_task.replace('+-', '-')
    new_task = new_task.replace('--', '+')
    new_task = parse_solution(new_task, q.random_domain)
    return_dict = {'question': new_task, 'variable_dictionary': variables_used, 'template_type': template_type,
                   'template_specific': template_specific, 'primary_key': primary_key,
                   'number_of_answers': number_of_answers, 'replacing_words': replacing_words}
    return return_dict


@Debugger
def get_question(user, template_id, topic=''):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 60
    increase = 15
    q = ''
    template_type = 'normal'
    if template_id == '':
        u = User.objects.get(username=user.username)
        user_rating = u.extendeduser.rating
        while True:
            q = Template.objects.filter(rating__gt=(user_rating-slack))
            q = q.filter(rating__lt=(user_rating+slack))
            q = q.filter(valid_flag=True)

            m = Template.objects.filter(choice_rating__gt=(user_rating-slack))
            m = m.filter(choice_rating__lt=(user_rating+slack))
            m = m.filter(valid_flag=True)
            m = m.filter(multiple_support=True)

            f = Template.objects.filter(fill_rating__gt=(user_rating-slack))
            f = f.filter(fill_rating__lt=(user_rating+slack))
            f = f.filter(valid_flag=True)
            f = f.filter(fill_in_support=True)

            if topic != '':
                q = q.filter(topic__topic__iexact=topic)
                f = f.filter(topic__topic__iexact=topic)
                m = m.filter(topic__topic__iexact=topic)

            # Use count instead of len as len loads the records.
            # Using len would be faster if we had to load all the records to python objects.
            length_normal = q.count()
            length_multiple = m.count()
            length_fill_in = f.count()
            length_total = length_fill_in + length_normal + length_multiple
            if length_total > 0:
                r_number = randint(1, length_total)
                if r_number <= length_fill_in and length_fill_in > 0:
                    q = f[r_number - 1]
                    template_type = 'blanks'
                elif r_number <= length_multiple + length_fill_in and length_multiple > 0:
                    template_type = 'multiple'
                    q = m[r_number - length_fill_in - 1]
                else:
                    q = q[r_number - length_fill_in - length_multiple - 1]
                break
            slack += increase

            if slack >= 800:
                q = Template.objects.all()
                q = q.latest('id')
                break
    else:
        q = Template.objects.get(pk=template_id)

    # test
    #b = Level.objects.all()
    #print(b)
    #print(b.filter(template__topic__topic__contains='Integrasjon'))
    return {'template': q, 'type': template_type}


@Debugger
def get_level_question(user, level):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 100
    increase = 15
    user_progress = add_level_to_user(user, level)
    user_rating = user_progress.level_rating
    while True:
        q = level.templates.all()
        q = q.filter(rating__gt=(user_rating-slack))
        q = q.filter(rating__lt=(user_rating+slack))
        q = q.filter(valid_flag=True)

        m = level.templates.all()
        m = m.filter(choice_rating__gt=(user_rating-slack))
        m = m.filter(choice_rating__lt=(user_rating+slack))
        m = m.filter(valid_flag=True)
        m = m.filter(multiple_support=True)

        f = level.templates.all()
        f = f.filter(fill_rating__gt=(user_rating-slack))
        f = f.filter(fill_rating__lt=(user_rating+slack))
        f = f.filter(valid_flag=True)
        f = f.filter(fill_in_support=True)

        # Use count instead of len as len loads the records.
        # Using len would be faster if we had to load all the records to python objects.
        length_normal = q.count()
        length_multiple = m.count()
        length_fill_in = f.count()
        length_total = length_fill_in + length_normal + length_multiple
        if length_total > 0:
            r_number = randint(1, length_total)
            if r_number <= length_fill_in and length_fill_in > 0:
                q = f[r_number - 1]
                template_type = 'blanks'
            elif r_number <= length_multiple + length_fill_in and length_multiple > 0:
                template_type = 'multiple'
                q = m[r_number - length_fill_in - 1]
            else:
                template_type = 'normal'
                q = q[r_number - length_fill_in - length_multiple - 1]
            break
        slack += increase

        if slack >= 800:
            q = Template.objects.all()
            q = q.latest('id')
            break
    return {'template': q, 'type': template_type}


@Debugger
def replace_variables_from_array(arr, s):
    """Takes a string and replaces variables in the string with ones from the array

    #Example: (['R10', '5', 'R1', '7'], 'example string R1 and R10') -> 'example string 7 and 5'
    :param arr: Array of variables
    :param s: String to replace variables in
    :return: String with replaced variables
    """
    for x in range(0, len(arr)-1, 2):  # Set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s


@Debugger
def generate_valid_numbers(template, random_domain_list, conditions, test):
    """Generates valid numbers using each variables random domain.

    Also makes sure all variables follows the given conditions.
    :param template: The template used.
    :param random_domain_list: List of the random domains.
    :param conditions: The conditions the variable have to follow.
    :param test: If true the function returns the domain_dict instead of variable_dict.
    :return: The current generated variables used in the template.
    """
    hardcoded_variables = ['R22R', 'R21R', 'R20R', 'R19R', 'R18R', 'R17R', 'R16R', 'R15R', 'R14R', 'R13R', 'R12R',
                           'R11R', 'R10R', 'R9R', 'R8R', 'R7R', 'R6R', 'R3R', 'R2R', 'R1R', 'R0R']
    domain_dict = {}
    variable_dict = {}
    counter = 0
    # Loops through all possible variable names, and generate a random number for it.
    # Adds the variables names and numbers to the 2 dictionaries and the string
    for i in range(len(hardcoded_variables)):
        if template.count(hardcoded_variables[i]) > 0:
            try:  # In case of index out of bounds it just uses the first element of the array
                random_domain = random_domain_list[counter].split()
            except IndexError:
                # Uses the first domain in case one was not provided.
                random_domain = random_domain_list[0].split()
            random_number = str(make_number(random_domain))
            domain_dict[hardcoded_variables[i]] = random_domain
            variable_dict[hardcoded_variables[i]] = random_number
            counter += 1  # Counter to iterate through the random domains
    if len(conditions) > 1:
        variable_dict = check_conditions(conditions, variable_dict, domain_dict)

    # lesser_than('R0 * 2 < 3', domain_dict, variable_dict) #for testing purposes
    if test:
        return domain_dict
    return variable_dict


@Debugger
def check_conditions(conditions, variable_dict, domain_dict):
    """A function that checks if the generated variables pass the conditions and generates new ones until they do.

    :param conditions: The conditions of the template.
    :param variable_dict: List of variables.
    :param domain_dict: the domain of the variables.
    :return: List of variables that pass the conditions of the given template.
    """
    conditions = remove_unnecessary(conditions)
    # Check conditions --> if false: change a variable -> check conditions
    inserted_conditions = string_replace(conditions, variable_dict)
    while not parse_expr(latex_to_sympy(inserted_conditions), transformations=standard_transformations +
                         (convert_xor, implicit_multiplication_application,), global_dict=None, evaluate=True):
        variable_to_change = choice(list(variable_dict.keys()))  # Chose a random key from variable_dict
        variable_dict[variable_to_change] = new_random_value(variable_to_change, domain_dict, 0, '')
        inserted_conditions = string_replace(conditions, variable_dict)
    return variable_dict


@Debugger
def string_replace(string, variable_dict):
    """Replaces variables in a string with numbers from a dict

    :param string: String with variables in it.
    :param variable_dict: a dictionary with variable names as keys and the number to replace them which as values.
    :return: String with numbers instead of variable names.
    """
    for key in variable_dict:
        string = string.replace(key, str(variable_dict[key]))
    return string


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


@Debugger
def add_level_to_user(user, level):
    print(user.username)
    print(level.name)
    try:
        user_progress = UserLevelProgress.objects.get(user=user, level=level)
    except UserLevelProgress.DoesNotExist:
        user_progress = UserLevelProgress()
        user_progress.user = user
        user_progress.level = level
        user_progress.save()
    return user_progress


