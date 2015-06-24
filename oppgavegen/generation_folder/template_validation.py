from oppgavegen.latex_translator import latex_to_sympy
from oppgavegen.models import Template
from oppgavegen.decorators import Debugger
from oppgavegen.generation_folder.calculate_parse_solution import parse_solution
from oppgavegen.generation_folder.utility import remove_unnecessary, string_replace
from oppgavegen.generation_folder.calculate_parse_solution import parse_solution, parse_answer
from sympy import *
from oppgavegen.generation import generate_valid_numbers

@Debugger
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


@Debugger
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