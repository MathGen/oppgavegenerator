from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen import generation
from datetime import datetime

def make_edit_context_dict(template_id):
    q = Template.objects.get(pk=template_id)
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
    topics = ""
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'template_id': template_id , 'answer' : answer, 'solution' : solution,
                    'question_text' : question_text, 'calculation_references' : calculation_references,
                    'choices' : choices, 'conditions' : conditions, 'fill_in' : fill_in,
                    'topic' : topic, 'random_domain' : random_domain, 'unchanged_ref' : unchanged_ref,
                    'topics' : topics, 'dictionary' : dictionary}
    return context_dict


def make_answer_context_dict(form_values):
    user_answer = form_values['user_answer']
    template_type = form_values['template_type']
    template_specific = form_values['template_specific']
    q = Template.objects.get(pk=form_values['primary_key'])
    variable_dictionary = form_values['variable_dictionary'].split('§')
    replacing_words = form_values['replacing_words']
    random_domain = q.random_domain

    if template_type != 'blanks':
        answer = generation.replace_variables_from_array(variable_dictionary, q.answer.replace('\\\\', '\\'))
    else:
        answer = generation.get_values_from_position(template_specific, q.solution.replace('\\\\', '\\'))
        answer = generation.replace_variables_from_array(variable_dictionary, answer)
    answer = generation.parse_answer(answer, random_domain)
    answer = answer.replace('`', '')
    answer = answer.split('§')
    solution = str((q.question_text).replace('\\\\', '\\')) + "\\n" + str(q.solution.replace('\\\\', '\\'))
    solution = generation.replace_variables_from_array(variable_dictionary, solution)
    solution = generation.parse_solution(solution, random_domain)
    if len(replacing_words) > 0:
        solution = generation.replace_words(solution, replacing_words)['sentence']
    # print(solution)
    user_answer = user_answer.split('§')  #if a string doesn't contain the split character it returns as a list with 1 element
    #print(user_answer)
    #We format both the user answer and the answer the same way.
    user_answer = [generation.after_equal_sign(x) for x in user_answer] #only get the values after the last equal sign.
    user_answer = generation.calculate_array(user_answer, random_domain)
    answer = [generation.after_equal_sign(x) for x in answer]
    answer = generation.calculate_array(answer, random_domain)

    correct_answer = generation.check_answer(user_answer, answer)
    if correct_answer:
        answer_text = "\\text{Du har svart riktig!}"
    else:
        answer_text = "\\text{Du har svart }" + '\\text{ og }'.join(user_answer) + "\\text{. Det er feil! Svaret er: }" + '\\text{ og }'.join(answer)

    solution = solution.replace('+-', '-')
    solution = solution.replace('--', '+')
    context_dict = {'title': "Oppgavegen", 'answer': str(answer_text), 'user_answer': user_answer, 'solution': solution, 'user_won' : correct_answer}
    return context_dict



def submit_template(template, user, update):
    print(template.pk)
    print(template.answer)
    if update:
        q = Template.objects.get(pk=template.pk)
        template.rating = q.rating
        template.times_failed = q.times_failed
        template.times_solved = q.times_solved
        template.creation_date = q.creation_date
        template.creator = q.creator
    else:
        template.rating = 1200
        template.times_failed = 0
        template.times_solved = 0
        template.creation_date = datetime.now()
        template.creator = user
    if len(template.fill_in) > 1:
        template.fill_in_support = True
    if len(template.choices) > 1:
        template.multiple_support = True
    template.save()
    message = generation.template_validation(template.pk)
    return message


def change_elo(template, user, user_won, type):
    """Changes the elo of both user and task depending on who won."""
    # Formula for elo: Rx = Rx(old) + prefactor *(W-Ex) where W=1 if wins and W=0 if x loses
    # and Ex is the expected probability that x will win.
    # Ea = (1+10^((Rb-Ra)/400))^-1
    # Eb = (1+10^((Ra-Rb)/400))^-1
    expected_user = (1+10**((template.rating-user.rating)/400))**(-1)
    expected_template = (1+10**((template.rating-user.rating)/400))**(-1)
    prefactor = 32 #This value should be adjusted according to elo of the user (lower for higher ratings..)

    if user_won:
        new_user_rating = user.rating + prefactor*(1-expected_user)
        new_template_rating = template.rating + prefactor*(0-expected_template)
    else:
        new_user_rating = user.rating + prefactor*(1-expected_user)
        new_template_rating = template.rating + prefactor*(0-expected_template)
    user.rating = new_user_rating
    user.save()
    template.rating = new_template_rating
    template.save()

    return

def cheat_check(user_answer, disallowed):
    """Checks whether the user has used symbols/functions that are not allowed"""
    standard_disallowed = ['int','test',"'",'§'] + disallowed.split('§')
    if disallowed is not None:
        standard_disallowed += disallowed.split('§')
    for c in standard_disallowed:
        if user_answer.contains(c):
            return True
    return False