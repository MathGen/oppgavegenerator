"""

Defines reusable functions often called from views.py

"""
from oppgavegen.models import Template, Topic, Tag
from datetime import datetime
from django.contrib.auth.models import User
from oppgavegen.answer_checker import check_answer
from oppgavegen.decorators import Debugger
from oppgavegen.generation_folder.calculate_parse_solution import parse_solution, calculate_array, parse_answer
from oppgavegen.generation_folder.fill_in import get_values_from_position
from oppgavegen.generation_folder.utility import after_equal_sign, replace_words, replace_variables_from_array
from oppgavegen.generation_folder.template_validation import template_validation
import json


def make_edit_context_dict(template_id):
    """Returns context dict for use on the edit page"""
    templatetags = []
    q = Template.objects.get(pk=template_id)
    for t in q.tags.all():
        templatetags.append(t.name)
    calculation_references = q.calculation_ref
    question_text = q.question_text_latex
    solution = q.solution_latex
    answer = q.answer_latex
    choices = q.choices_latex
    conditions = q.conditions_latex
    fill_in = q.fill_in_latex
    topic = q.topic
    random_domain = q.random_domain
    unchanged_ref = q.unchanged_ref
    dictionary = q.dictionary
    used_variables = q.used_variables
    topics = ""
    tags = json.dumps(templatetags)
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'template_id': template_id, 'answer': answer, 'solution': solution,
                    'question_text': question_text, 'calculation_references': calculation_references,
                    'choices': choices, 'conditions': conditions, 'fill_in': fill_in,
                    'topic': topic, 'random_domain': random_domain, 'unchanged_ref': unchanged_ref,
                    'topics': topics, 'dictionary': dictionary, 'used_variables': used_variables,
                    'tags': tags}
    return context_dict


def make_answer_context_dict(form_values):
    """Returns context dict for use on the answer page"""
    user_answer = form_values['user_answer']
    template_type = form_values['template_type']
    template_specific = form_values['template_specific']
    q = Template.objects.get(pk=form_values['primary_key'])
    variable_dictionary = form_values['variable_dictionary'].split('§')
    replacing_words = form_values['replacing_words']
    random_domain = q.random_domain

    if template_type != 'blanks':
        answer = replace_variables_from_array(variable_dictionary, q.answer.replace('\\\\', '\\'))
    else:
        answer = get_values_from_position(template_specific, q.solution.replace('\\\\', '\\'))
        answer = replace_variables_from_array(variable_dictionary, answer)

    answer = parse_answer(answer, random_domain)
    answer = answer.replace('`', '')
    answer = answer.split('§')
    solution = str(q.question_text.replace('\\\\', '\\')) + "§" + str(q.solution.replace('\\\\', '\\'))
    solution = replace_variables_from_array(variable_dictionary, solution)
    solution = parse_solution(solution, random_domain)
    if len(replacing_words) > 0:
        solution = replace_words(solution, replacing_words)['sentence']
    user_answer = user_answer.split('§')  # If a string doesn't contain the character it returns a list with 1 element
    # We format both the user answer and the answer the same way.
    user_answer = [after_equal_sign(x) for x in user_answer]  # Only get the values after last equal sign.
    user_answer = calculate_array(user_answer, random_domain)
    answer = [after_equal_sign(x) for x in answer]
    answer = calculate_array(answer, random_domain)
    answer_text = "\\text{Du har svart }" + '\\text{ og }'.join(user_answer) + \
                      "\\text{. Det er feil! Svaret er: }" + '\\text{ og }'.join(answer)

    correct_answer = check_answer(user_answer, answer, template_type)  # Check if the user answered correctly.

    if correct_answer:
        answer_text = "\\text{Du har svart riktig!}"

    solution = solution.replace('+-', '-')
    solution = solution.replace('--', '+')
    solution = solution.replace('- -', '+')
    solution = solution.replace('+ -', '-')
    answer_text = latex_exceptions(answer_text)
    context_dict = {'title': "Oppgavegen", 'answer': str(answer_text),
                    'solution': solution, 'user_won': correct_answer}
    return context_dict


def submit_template(template, user, update, newtags=None):
    """Submits or updates a template to the database (depending on if update is true or not)"""
    # taglist = validate_tags(template.tags)
    if update:
        q = Template.objects.get(pk=template.pk)
        template.rating = q.rating
        template.choice_rating = q.choice_rating
        template.fill_rating = q.fill_rating
        template.times_failed = q.times_failed
        template.times_solved = q.times_solved
        template.creation_date = q.creation_date
        template.creator = q.creator
        #template.tags = q.tags.all() todo: remove this as well ( or fix)
        template.name = q.name
        template.difficulty = q.difficulty
    else:
        template.rating = 1200
        template.fill_rating = 1150
        template.choice_rating = 1100
        template.times_failed = 0
        template.times_solved = 0
        template.creation_date = datetime.now()
        template.creator = user
    if len(template.fill_in) > 1:
        template.fill_in_support = True
    if len(template.choices) > 1:
        template.multiple_support = True
    template.save()
    template.tags.clear()
    template.tags = newtags
    message = template_validation(template.pk)
    return message


def cheat_check(user_answer, disallowed):
    """Checks whether the user has used symbols/functions that are not allowed"""
    standard_disallowed = ['int', 'test', "'", '@']
    if disallowed is not None and disallowed != '':
        standard_disallowed = standard_disallowed + disallowed.split('§')
    for s in standard_disallowed:
        if s in user_answer:
            return True
    return False


def latex_exceptions(string):
    """Replaces wrong latex with the proper one"""
    string = string.replace('\\tilde', '\\sim')
    return string


def validate_tags(tags):
    # template = Template.objects.get(pk=template_id)
    taglist = []
    for e in tags:
        if e in Tag.objects.all():
            taglist.append(e)
        else:
            tag = Tag.objects.new(name=e)
            taglist.append(tag)
    return taglist

