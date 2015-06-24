from oppgavegen.decorators import Debugger
from random import shuffle
from oppgavegen.generation import string_replace

@Debugger
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