from oppgavegen.models import *
import json


def format_domain():
    """Formats the random_domain for templates from the old format to the new one."""
    templates = Template.objects.all()
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w']
    hardcoded_variables = ['R0R', 'R1R', 'R2R', 'R3R', 'R4R', 'R5R', 'R6R', 'R7R', 'R8R', 'R9R', 'R10R',
                           'R11R', 'R12R', 'R13R', 'R14R', 'R15R', 'R16R', 'R17R', 'R18R', 'R19R', 'R20R', 'R21R', 'R22R']

    for t in templates:
        try:
            variables_used = (t.used_variables).split()
        except Exception:
            pass

        variable_list = []
        try:
            for x in variables_used:
                variable_list.append(hardcoded_variables[letters.index(x.split('§')[1])])
        except Exception:
            pass

        domain_list = t.random_domain.split('§')
        domain_dict = {}
        counter = 0
        for x in reversed(domain_list):
            try:
                domain_dict[variable_list[counter]] = [x, False]
            except Exception:
                domain_dict[hardcoded_variables[counter]] = [x, False]
            counter += 1

        t.random_domain = json.dumps(domain_dict)
        t.save()
    return