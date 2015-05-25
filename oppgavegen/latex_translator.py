"""

Defines functions needed to translate LaTeX Math-expressions
to expressions compatible with SymPy

"""

def latex_to_sympy(expr):
    """Takes a latex expression and returns a expression sympy can use"""
    expr = expr.replace('\\ne', '!=')
    expr = expr.replace('{', '(')
    expr = expr.replace('}', ')')
    expr = expr.replace('\\cdot', '*')
    expr = expr.replace('\\times', '*')
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

    expr = expr.replace('x', ' x')
    expr = expr.replace('y', ' y')
    expr = expr.replace('z', ' z')
    expr = expr.replace('  ', ' ')  # Remove double whitespace
    expr = expr.replace('ma x (', 'Max(')
    expr = expr.replace('ma x(', 'Max(')
    expr = expr.replace('min (', 'Min(')
    expr = expr.replace('min(', 'Min(')

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
    expr = expr.replace('\\', '')
    expr = expr.replace('frac', '')
    expr = expr.replace('binom', 'binomial')
    expr = parenthesis_around_minus(expr)
    return expr

def parenthesis_around_minus(expression):
    """Takes a expression and returns it with parenthesis around numbers with - where needed."""
    exceptions = '0123456789.)(xyz'
    expression += ' ' #add a empty space at the end of the string to avoid error.
    new_expr = expression
    count = 0
    record = False
    difference = 0
    for i in range(0, len(expression)):
        if expression[i] == '-' and expression[i-1] not in exceptions:
            record = True
        elif record and expression[i] not in exceptions:
            record = False
            if count > 0:
                insert_start = i-count+difference-1
                t_i = i + difference
                new_expr = new_expr[:insert_start] + '(' + new_expr[insert_start:t_i] + ')' + new_expr[t_i:len(new_expr)]
                difference += 2
                count = 0
        elif record:
            count += 1
    return new_expr