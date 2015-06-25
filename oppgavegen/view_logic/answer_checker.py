"""

Defines functions needed to evaluate user input

"""

from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy


def check_answer(user_answer, answer, template_type):
    """Checks if the answer the user gave is correct.

    :param user_answer: A list containing the answer(s) the user gave.
    :param answer: A list containing the answer(s) to the template.
    :param template_type: A string detailing how the template is presented.
    :return: Boolean of whether the answer is correct
    """

    if template_type != 'normal':
        # Reverse iteration to avoid index out of bounds when elements get deleted.
        for s in range(len(answer)-1, -1, -1):
                if parse_using_sympy(latex_to_sympy(answer[s]) + '==' + latex_to_sympy(user_answer[s])):
                    del user_answer[s]

    else:
        for s in answer:
            for us in user_answer:
                if parse_using_sympy(latex_to_sympy(s) + '==' + latex_to_sympy(us)):
                    user_answer.remove(us)
                    break

    if user_answer == []:  # Can not be written as user_answer is [], so don't pep this.
        right_answer = True
    else:
        right_answer = False
    return right_answer


def parse_using_sympy(s):
    transformations = standard_transformations + (convert_xor, implicit_multiplication_application,)
    return parse_expr(s, transformations=transformations, global_dict=None, evaluate=True)