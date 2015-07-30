from sympy import simplify
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy


def parenthesis_remover(s):
    """removes parenthesises from expressions and checks if the expression is still valid."""
    pairs = find_pairs(s, '(', ')')
    removable = []
    for pair in pairs:
        temp_s =  remove_all_from_list(s, pair)
        if  parse_using_sympy(latex_to_sympy(temp_s) + '==' + latex_to_sympy(s)):
            removable.append(pair[0])
            removable.append(pair[1])
    s = remove_all_from_list(s, removable)
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
    :param string: The string to look for pairs in.
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

    # while i < len(s):  # Logic for inserting a / in fractals
    #     if s[i] == 'c' and s[i-1] == 'a' and s[i-2] == 'r' and s[i-3] == 'f' and s[i-4] == '\\':
    #         recorder = True
    #     if recorder:
    #         if s[i] == '(':
    #             counter += 1
    #         elif s[i] == ')':
    #             counter -= 1
    #         if s[i] == ')' and counter == 0:
    #             s = s[0:i+1] + "/" + s[i+1:len(s)]
    #             recorder = False
    #     i += 1

def parse_using_sympy(s):
    transformations = standard_transformations + (convert_xor, implicit_multiplication_application,)
    return parse_expr(s, transformations=transformations, global_dict=None, evaluate=True)