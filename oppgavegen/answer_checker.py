"""

Defines functions needed to evaluate user input

"""

from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)
from oppgavegen.latex_translator import latex_to_sympy

def check_answer(user_answer, answer):
    """Checks if the answer the user gave is correct.

    :param user_answer: A list containing the answer(s) the user gave
    :param answer: A list containing the answer(s) to the template
    :return: Boolean of whether the answer is correct
    """
    for s in answer:
        for us in user_answer:
            if parse_expr(latex_to_sympy(s) + '==' + latex_to_sympy(us), transformations=standard_transformations +
                          (convert_xor, implicit_multiplication_application,), global_dict=None, evaluate=True):
                user_answer.remove(us)
                break

    if user_answer == []:  # Can not be written as user_answer is []
        right_answer = True
    else:
        right_answer = False
    return right_answer