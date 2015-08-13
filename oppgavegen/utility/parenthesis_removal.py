from sympy import simplify
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy


def parenthesis_removal(s):

    split_list = ['=', '§', '\\arrow', '\\and', '\\or', '\\union', '\\intersection', '\\rightarrow', '\\leftarrow'
                  '\\leftrightarrow']
    replace_dict = make_replace_text_dict(s)
    print('b<<')
    print(replace_dict)
    s = replace_value_with_key(s, replace_dict)
    split_list.extend(replace_dict.keys())
    s_list = splitter(s, split_list)
    new_s = ''
    for x in range(0, len(s_list), 2):
        if x > len(s_list) - 1:
            break
        new_s += parenthesis_remover(s_list[x])
        if x < len(s_list) - 1:
            new_s += s_list[x+1]

    new_s = replace_key_with_value(new_s, replace_dict)
    new_s = fix_multiply_minus(new_s)
    return new_s


def parenthesis_remover(s):
    """removes parenthesises from expressions and checks if the expression is still valid."""
    #replace_dict = make_replace_text_dict(s)
    #s = replace_value_with_key(s, replace_dict)
    s = s.replace(')(', ')*(')
    s = s.replace('§', '+paragraftegn+')
    s = s.replace('(+', '(')
    s = s.replace('(+', '(')

    pairs = find_pairs(s, '(', ')')
    removable = []
    for pair in pairs:
        temp_s =  remove_all_from_list(s, pair)
        try:
            #  Note: +0 is added so the string never ends with + (which would stop sympy)
            if  parse_using_sympy(latex_to_sympy(temp_s) + '+0' + '==' + latex_to_sympy(s) + '+0'):
                removable.append(pair[0])
                removable.append(pair[1])
        except Exception as e:
            print('exception in parenthesis remover:')
            print(e)
            print(s)
            print('^ string that failed. end of exception.')

    s = remove_all_from_list(s, removable)
    #s = replace_key_with_value(s, replace_dict)
    s = s.replace('+parenthesisleft+', '(')
    s = s.replace('+parenthesisright+', ')')
    s = s.replace('+erlik+', '=')
    s = s.replace('+paragraftegn+', '§')

    s = s.replace('+-', '-')
    s = s.replace('--', '+')
    s = s.replace('- -', '+')
    s = s.replace('+ -', '-')

    s = s.replace('§+', '§')
    s = s.replace('=+', '=')
    s = s.replace('^{+', '^{')
    s = s.replace('(+', '(')

    return s


def remove_all_from_list(s, list):
    """Removes from s all the positions in the list ie. 'abcd', [1,2] -> 'ad'."""
    list.sort(reverse=True)  # Reverse list to avoid using a offset after removing characters.
    for i in list:
        s = remove_character(s, i)
    return s


def remove_character(s, position):
    """Removes the character at the given position ie. 'abc', 1 -> 'ac'"""
    s = s[0:position] + s[position+1:len(s)]
    return s


def find_pairs(s, one, two):
    """
    :param s: The string to look for pairs in.
    :param one: The first of a pair.
    :param two: The second of a pair.
    :return: returns a list of pairs.
    """
    counter = 0
    pairs = []
    for i in range(0, len(s)):
        if s[i] == one:
            for j in range(i+1, len(s)):
                if s[j] == two and counter == 0:
                    pairs.append([i, j])
                    counter = 0
                    break
                if s[j] == one:
                   counter += 1
                elif s[j] == two:
                    counter -= 1
    return pairs


def parse_using_sympy(s):
    transformations = standard_transformations + (convert_xor, implicit_multiplication_application,)
    return parse_expr(s, transformations=transformations, global_dict=None, evaluate=True)


def make_replace_text_dict(s):
    """Makes a dictionary used for replacing latex text in a string"""
    #Technicly this function isn't perfect, for instance if someone put a stray } or { inside their text.
    #However if they did it would also break mathquill/latex so the function is good enough (heuristic).
    print(s)
    record = False
    count = 0
    start = 0
    text_dict = {}
    for i in range(0, len(s)):
        if record is False:
            if s[i-5:i+1] == '\\text{':
                start = i-5
                count = 0
                record = True

        elif record is True and s[i] == '}':
            if count == 0:
                end = i+1  # Redundant
                text_dict['+text' + str(start) + '+'] = s[start:end]
                record = False
            else:
                count -= 1

        elif record is True and s[i] == '{':
            count += 1

    print('a<<')
    print(text_dict)
    return text_dict


def replace_value_with_key(s, replace_dict):
    """In string s values in the dict get replaced with their key"""
    for key in replace_dict:
        s = s.replace(replace_dict[key], key)
    return s


def replace_key_with_value(s, replace_dict):
    """In string s keys in the dict get replaced with their value"""
    for key in replace_dict:
        s = s.replace(key, replace_dict[key])
    return s

def remove_redudant_pluss(s):
    # define some rules
    if s[0] == '+':
        s = s[1:]

    return s


def fix_multiply_minus(s):
    # Fixes instances where *-... appears. (It should be *(-...)  )
    allowed = 'abcdefghijklmnopqrstuvwxyz123456789'
    record = False
    counter = 0
    difference = 0
    s += ' '  # add a whitespace to avoid end of string bugs.
    new_s = s
    for i in range(0, len(s)):
        if record == True:
            if s[i] not in allowed:
                print(counter)
                print(s[i])
                if counter > 0:
                    start = i - 1 - counter + difference
                    end = i
                    new_s = new_s[0:start] + '(' + new_s[start:end] + ')' + new_s[end:]
                    difference += 2
                record = False
            else:
                counter += 1
        if s[i-1] == '*' and s[i] == '-':
            record = True

    return new_s


def find_occurrences(s, left, right,  left_skip='', right_skip=''):
    # Finds a occurrence (left, right) in a string and returns a list of start and end positions.
    # left and right skip are used for occurrences that have some sort of nesting.
    # For instance \text{} needs to check for nesting of {} and end the occurrence when a } is found at the outer level.
    if s == '':
        return []
    position_list = []
    record = False
    count = 0
    start = 0

    for i in range(0, len(s)):
        if record is False:
            if s[i:i+len(left)] == left:
                start = i
                count = 0
                record = True

        elif record is True and s[i] == left_skip:
            if count == 0:
                end = i+1  # Redundant

            else:
                count -= 1

        elif record is True and s[i] == right_skip:
            count += 1

    return position_list

def splitter(s, split_list):
    """ Splits string into smaller substring according to a list. """
    # Note: This function won't work correctly if there exists splittable substrings of other splittable strings
    # An example would be if 'banana' was a split string and 'nana' also was one.
    # However there is no practical example where this is the case, ie. the function works for all current cases.
    # (Since most cases are latex this won't really happen as all of latex functions start with \)
    # for example 'or' is a substring that would occur in a lot of places, but '\or' won't.
    # The people making latex probably had this in mind when designing their language.
    split_dict = {}
    split_indexes = []
    new_list = []
    for split in split_list:
       for i in range(len(s)):
           if s.startswith(split, i):
               split_indexes.append(i)
               split_dict[i] = split

    start = 0
    split_indexes.sort()
    for split_index in split_indexes:
        new_list.append(s[start:split_index])
        new_list.append(split_dict[split_index])
        start = split_index + len(split_dict[split_index])
    new_list.append(s[start:])
    # new_list = filter(None, new_list)
    return new_list

