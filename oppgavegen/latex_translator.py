"""

Defines functions needed to translate LaTeX Math-expressions
to expressions compatible with SymPy

"""

def latex_to_sympy(expr):
    """Takes a latex expression and returns a expression sympy can use"""
    expr = expr.replace('\\ne', '!=')
    expr = expr.replace('{', '(') # SymPy doesn't really use {} in most cases.
    expr = expr.replace('}', ')')
    expr = expr.replace('\\cdot', '*')
    expr = expr.replace('\\times', '*')
    expr = expr.replace('\\left[\\begin(matrix)', '\\begin(matrix)')
    expr = expr.replace('\\end(matrix)\\right]', '\\end(matrix)')
    expr = expr.replace('\\left', '')
    expr = expr.replace('\\right', '')
    expr = expr.replace('∨', '|')
    expr = expr.replace('∧', '&')
    expr = expr.replace('text( )', ' ')
    expr = expr.replace('arcsin', 'asin')
    expr = expr.replace('arccos', 'acos')
    expr = expr.replace('arctan', 'atan')
    expr = expr.replace('arcsec', 'asec')
    expr = expr.replace('arccosec', 'acsc')
    expr = expr.replace('arccosec', 'acsc')
    expr = expr.replace('arccot', 'acot')
    expr = expr.replace('cosec', 'csc')
    expr = expr.replace('int', 'integrate')
    expr = expr.replace('\\begin{equation*}', '')
    expr = expr.replace('\\end{equation*}', '')

    expr = expr.replace('x', ' x') # Add space before variables to prvenet sympy fuckups
    expr = expr.replace('y', ' y')
    expr = expr.replace('z', ' z')
    expr = expr.replace('  ', ' ')  # Remove double whitespace
    # Fix expressions broken by the space
    expr = expr.replace('ma x (', 'Max(')
    expr = expr.replace('ma x(', 'Max(')
    expr = expr.replace('min (', 'Min(')
    expr = expr.replace('min(', 'Min(')
    expr = expr.replace('matri x', 'matrix')

    if expr[0] == '*':
        expr = expr[1:]

    i = 0
    counter = 0
    recorder = False
    # Todo: Make a function that does this that can be used for both frac and binom
    while i < len(expr):  # Logic for inserting a / in fractals
        if expr[i] == 'c' and expr[i-1] == 'a' and expr[i-2] == 'r' and expr[i-3] == 'f' and expr[i-4] == '\\':
            recorder = True
        if recorder:
            if expr[i] == '(':
                counter += 1
            elif expr[i] == ')':
                counter -= 1
            if expr[i] == ')' and counter == 0:
                expr = expr[0:i+1] + "/" + expr[i+1:len(expr)]
                recorder = False
        i += 1
    i = 0
    counter = 0
    while i < len(expr):  # Logic for making \binom(a/b) -> binomial(a,b)
        if expr[i] == 'o' and expr[i-1] == 'n' and expr[i-2] == 'i' and expr[i-3] == 'b' and expr[i-4] == '\\':
            recorder = True
        if recorder:
            if expr[i] == '(':
                counter += 1
            elif expr[i] == ')':
                counter -= 1
            if expr[i] == ')' and counter == 0:
                expr = expr[0:i] + "," + expr[i+2:len(expr)]
                recorder = False
        i += 1

    expr = pmatrix_to_matrix(expr)
    expr = pmatrix_to_matrix(expr, '\\begin(matrix)', '\\end(matrix)')
    expr = expr.replace('\\', '')
    expr = expr.replace('frac', '')
    expr = expr.replace('binom', 'binomial')
    expr = parenthesis_around_minus(expr)
    return expr


def parenthesis_around_minus(expression):
    """Takes a expression and returns it with parenthesis around numbers with - where needed."""
    exceptions = '0123456789.)({}xyz=+-?/'  # Having xyz in exceptions might introduce a bug in some situations
    expression += ' ' #add a empty space at the end of the string to avoid error.
    new_exp = expression
    count = 0
    record = False
    difference = 0
    for i in range(1, len(expression)):
        if expression[i] == '-' and expression[i-1] not in exceptions:
            record = True
        elif record and expression[i] not in exceptions:
            record = False
            if count > 0:
                insert_start = i-count+difference-1
                t_i = i + difference
                new_exp = new_exp[:insert_start] + '(' + new_exp[insert_start:t_i] + ')' + new_exp[t_i:len(new_exp)]
                difference += 2
                count = 0
        elif record:
            count += 1
    return new_exp

def remove_pm_and_add_parenthesis(expr):
    expr = expr.replace('+-', '-')
    expr = expr.replace('--', '+')
    expr = parenthesis_around_minus(expr)
    expr = expr.replace('+-', '-')
    expr = expr.replace('--', '+')
    return expr

# Note: Remember that {} is swapped for () in latex_to_sympy
def pmatrix_to_matrix(m, start_string='\\begin(pmatrix)', end_string='\\end(pmatrix)',
                      replace_start=' Matrix([[', replace_end=']]) ', replace_list=None):
    """
    Converts a sympy latex Matrix into a mathquill latex matrix.
    :param m: a string with or without a matrix in it
    :param replace_start: a string with information as to what the replaced string should start with
    :param replace_end: a string with information as to what the replaced string should end with
    :param replace_list: A list with lists of strings to replace
    :param start_string: String of what the matrix starts with
    :param end_string: String of what the matrix starts with
    :return: Returns a string which has had its Matrices converted to SymPy format.
    """
    if replace_list is None: # This is done because lists are mutable, and therefore bad to use as default args.
        replace_list = [['&',', '], ['\\\\','], [']]

    index_start = find_indexes(m, start_string)
    while index_start != []: # Don't listen to pep, don't simplify
        index_end = find_indexes(m, end_string)
        index_end = sort_nesting(index_start, index_end)
        start = index_start[0] + len(start_string)
        end = index_end[0]
        temp_m = m[start:end]
        for s in replace_list:
            temp_m = temp_m.replace(s[0], s[1])
        temp_m = replace_start + temp_m + replace_end
        m = m[:start-len(start_string)] + temp_m + m[end+len(end_string):]
        index_start = find_indexes(m, start_string)
    return m


def find_indexes(s, index):
    """Finds all the given indexes of a given string"""
    index_list = [n for n in range(len(s)) if s.find(index, n) == n]
    return index_list


def sort_nesting(list1, list2):
    """Takes a list of start points and end points and sorts the second list according to nesting"""
    temp_list = []
    while list2 != temp_list:
        temp_list = list2[:] # Make a copy of list2 instead of reference
        for i in range(1, len(list1)):
            if list2[i] > list2[i-1] and list1[i] < list2[i-1]:
                list2[i-1], list2[i] = list2[i], list2[i-1]
    return list2


def sympy_to_mathquill(expr): # Might not be needed
    expr = expr.replace('\\begin{equation*}', '')
    expr = expr.replace('\\end{equation*}', '')
    expr = expr.replace('{matrix}', '{pmatrix}')
    return expr