"""

Handles task generation from templates.

"""

from random import randint, uniform, shuffle, choice
from math import floor, copysign
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy
from .models import Template, Level, UserLevelProgress
from django.contrib.auth.models import User


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
        print(fill_in_dict)
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


def calculate_answer(s, domain):
    """Calculates a string using sympy.

    :param s: String to be calculated
    :param domain: The domain of the variables.
    :return: A latex version of the calculated string.
    """
    if not is_number(s):  # Small optimization
        s = remove_unnecessary(s)
        s = str(latex_to_sympy(s))
        s = parse_expr(s, transformations=standard_transformations +
                       (convert_xor, implicit_multiplication_application,), global_dict=None, evaluate=False)
        s = latex(sympify(str(s)))
        # Sometimes sympify returns the value 'zoo'
    else:
        s = round_answer(domain, float(s))
    return str(s)


def parse_solution(solution, domain):
    """Parses a solution (or other similar string) and calculates where needed. (between @? ?@)

    :param solution: The string to be parsed.
    :param domain: The domain of the different variables.
    :return: A parsed version of the input string (solution)
    """
    arr = []
    new_arr = []
    recorder = False
    new_solution = solution
    b = s = ''
    for c in solution:
        if b == '@' and c == '?':
            recorder = True
            s = ''
        elif b == '?' and c == '@':
            recorder = False
            arr.append(s[:-1])
        elif recorder is True:
            s += c
        b = c
    for x in range(len(arr)):
        new_arr.append(calculate_answer(str((arr[x])), domain))
        r = '@?' + arr[x] + '?@'
        new_solution = new_solution.replace(r, new_arr[x])
    print(new_solution)
    return new_solution


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
    return {'template' : q, 'type' : template_type}

def get_level_question(user, level):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 60
    increase = 15
    user_progress = add_level_to_user(user, level)
    user_rating = user_progress.level_rating

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

    # test
    #b = Level.objects.all()
    #print(b)
    #print(b.filter(template__topic__topic__contains='Integrasjon'))
    return {'template' : q, 'type' : template_type}


def replace_words(sentence, dictionary):
    """
    Replaces variables in a string with the value of a key in the given dictionary.
    Example: ('example sentence', 'example § apple, grape') ->
             {'sentence': 'apple sentence', 'replace_string' 'example § apple'}}
    :param sentence: String to replace words in.
    :param dictionary: A splittable (§) string with word alternatives.
    :return: dictionary with the new sentence and a splittable string with what words were replaced
    """
    dictionary = dictionary.split('§')
    replace_string = ''
    for i in range(0, len(dictionary)-1, 2):
        replace_strings = dictionary[i+1].split(',')
        replace_word = replace_strings[randint(0, len(replace_strings)-1)]
        sentence = sentence.replace(dictionary[i], replace_word)
        replace_string += '§' + dictionary[i] + '§' + replace_word
    return {'sentence': sentence, 'replace_string': replace_string[1:]}


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
    for x in range(0, len(arr)-1, 2):  # Set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s


def parse_answer(answer, domain):
    """Parses the answer. works for arrays with multiple answers."""
    answer = answer.split('§')
    counter = 0
    for s in answer:
        answer[counter] = parse_solution(s, domain)
        if answer[counter] == 'zoo':
            answer = ['error']  # This is an array so that join doesn't return e§r§r§o§r
            continue
        counter += 1
    return '§'.join(answer)  # join doesn't do anything if the list has 1 element, except converting it to str


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


def dict_to_string(variable_dict):
    """Returns a separated string of the key and value pairs of a dict"""
    variables_used = ""
    for key in variable_dict:
        variables_used += '§' + str(key) + '§' + str(variable_dict[key])
    return variables_used[1:]  # Use [1:] to remove unnecessary § from the start


def array_to_string(array):
    """Turns a array into a string separated by §."""
    string = ''
    for s in array:
        string += '§' + s
    return string[1:]  # Use [1:] to remove unnecessary § from the start


def remove_unnecessary(string):
    """Removes unnecessary symbols from a string and returns the string."""
    string = string.replace('@?', '')
    string = string.replace('?@', '')
    return string


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


def string_replace(string, variable_dict):
    """Replaces variables in a string with numbers from a dict

    :param string: String with variables in it.
    :param variable_dict: a dictionary with variable names as keys and the number to replace them which as values.
    :return: String with numbers instead of variable names.
    """
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


def fill_in_the_blanks(fill_in):
    """Returns a fill in the blank template and the position of the holes."""
    hole_dict = find_holes(fill_in)
    make_holes_dict = make_holes(hole_dict, fill_in)
    hole_positions = list(hole_dict.keys())
    hole_positions = array_to_string(hole_positions)
    fill_in = make_holes_dict['fill_in']
    return_dict = {'fill_in': fill_in, 'hole_positions': hole_positions}
    return return_dict


def find_holes(fill_in):
    """Finds the available holes in the template and their position."""
    #fill_in = fill_in.split('§')  # Makes fill in into a list.
    #fill_in = fill_in[len(fill_in)-1]
    hole_dict = {}  # Keeps track of what is getting replaced and the position of that in the string.
    recorder = False
    counter = 0  # Keeps track of how far in the string the loop is
    start_point = 0  # Start point of box
    a = b = c = d = e = s = ''  # Used to keep track of the last 5 variables iterated over.
    # Note: it might be faster/better to use a counter instead of storing previous characters in the for loop.
    # ie. for x in range(0, len(fill_in). See latex_to_sympy for this in action.
    for f in fill_in:
        if a == '@' and b == 'x' and c == 'x' and d == 'x' and e == 'x' and f == '@':
            recorder = not recorder  # Flip recorder
            if recorder:
                counter -= 6  # Sets the counter back 6 to compensate for @xxxx@ which is not in the original string
                start_point = counter+1
                if counter < len(fill_in):
                    if fill_in[counter] == '{' or fill_in[counter] == '(':  # This is to avoid a specific bug
                        start_point = counter
            elif not recorder:
                end_point = counter-5
                # Swapping
                # Hole_dict[s[:-5]] = str(start_point) + ' ' + str(end_point-5)
                print(start_point)
                hole_dict[str(start_point) + ' ' + str(end_point)] = s[:-5]

                counter -= 6  # Sets the counter back 6 to compensate for @xxxx@ which is not in the original string
            s = ''
        elif recorder is True:
            s += f
        counter += 1
        a = b
        b = c
        c = d
        d = e
        e = f
    print(hole_dict)
    return hole_dict


def make_holes(hole_dict, fill_in):
    """Inserts holes at given places in the template for fill in the blanks

    :param hole_dict: dictionary of the holes to replace.
    :param fill_in: the template.
    :return: dictionary with fill in the blanks template with holes and which holes were replaced.
    """
    holes_to_replace = list(hole_dict.values())
    for s in holes_to_replace:
        fill_in = fill_in.replace('@xxxx@'+s, '\\MathQuillMathField{}'+'@xxxx@')
    fill_in = fill_in.replace('@xxxx@', '')
    return_dict = {'fill_in': fill_in, 'holes_replaced': holes_to_replace}
    return return_dict


def get_values_from_position(position_string, solution):
    """Takes a string of positions and returns a values from the string with those positions"""
    position_array = position_string.split('§')
    values = ''
    for s in sorted(position_array):
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
        if choices[x].count(possible_holes[0]) > 0:
            choices[x] = choices[x].replace(possible_holes[0], '\\MathQuillMathField{}')
        else:
            for z in range(1, len(possible_holes)):
                if choices[x].count(possible_holes[z]) > 0:
                    choices[x] = choices[x].replace(possible_holes[z], '\\MathQuillMathField{}')
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
    for x in range(0, 10000):
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
    got_trough_test = 0  # 1 if template got through test, and 0 if not.
    # Make numbers, check condition, check calculations
    random_domain = template.random_domain
    random_domain_list = random_domain.split('§')
    # Efficiency note: it might be faster to pass the domain list, instead of getting them from template every time.
    answer = template.answer
    question = template.question_text
    solution = template.solution
    conditions = template.conditions
    conditions = remove_unnecessary(conditions)

    variable_dict = generate_valid_numbers(question, random_domain_list, "", False)
    inserted_conditions = string_replace(conditions, variable_dict)
    if len(conditions) > 1:
        conditions_pass = sympify(latex_to_sympy(inserted_conditions))
    else:
        conditions_pass = True
    if conditions_pass:
        answer = string_replace(answer, variable_dict)
        solution = string_replace(solution, variable_dict)

        try:
            answer = parse_answer(answer, random_domain)
            parse_solution(solution, random_domain)  # Checks if solution can be parsed
            got_trough_test = 1
        except Exception:
            pass
        if answer == 'error':
            got_trough_test = 0
    return got_trough_test


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
    answer = float(answer)  # Cast it to float. if it is a integer, it will get rounded back to a integer.
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
        answer = custom_round(answer, rounding_number)
        if answer.is_integer():
            answer = custom_round(answer)
    else:
        answer = custom_round(answer)
    return answer


def custom_round(x, d=0):
    """
    Python 3.x rounding function uses bankers rounding, which is note the same as method of rounding
    A math student would expect. This round function rounds in the expected way. ie. 2.5 = 3 and 1.5 = 2.
    :param x: the number to be rounded.
    :param d: number of decimals.
    :return the rounded version of x.
    """
    p = 10 ** d
    round_x = float(floor((x * p) + copysign(0.5, x)))/p
    if d == 0:
        round_x = int(round(x))
    return round_x


def add_level_to_user(user, level):
    user_progress = UserLevelProgress.objects.get(user=user, level=level)
    if not user_progress:
        user_progress = UserLevelProgress()
        user_progress.user = user
        user_progress.level = level
        user_progress.save()
    return user_progress
