from math import copysign

from sympy import *

from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

from oppgavegen.utility.decorators import Debugger
from oppgavegen.utility.utility import is_number, remove_unnecessary
from oppgavegen.latex_translator import latex_to_sympy


@Debugger
def calculate_answer(s, domain):
    """Calculates a string using sympy.

    :param s: String to be calculated
    :param domain: The domain of the variables.
    :return: A latex version of the calculated string.
    """
    try:
        if not is_number(s):  # Small optimization
            s = remove_unnecessary(s)
            s = str(latex_to_sympy(s))
            s = s.replace('*)', ')*')
            s = s.replace('?)@', ')?@')
            s = parse_expr(s, transformations=standard_transformations +
                           (convert_xor, implicit_multiplication_application,), global_dict=None, evaluate=False)
            s = latex(sympify(str(s)))
            # Sometimes sympify returns the value 'zoo'
        else:
            s = round_answer(domain, float(s))
    except Exception as e:
        print('exception in calculate answer')
        print(e)
    return str(s)


@Debugger
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

    count = 0
    for x in range(len(arr)):
        if(arr[x]):
            new_arr.append(calculate_answer(str((arr[x])), domain))
            r = '@?' + arr[x] + '?@'

            try:
                new_solution = new_solution.replace(r, new_arr[x-count])
            except:
                pass
        else:
            count += 1
    print('exiting parse solution')
    return new_solution


@Debugger
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


@Debugger
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


@Debugger
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


@Debugger
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