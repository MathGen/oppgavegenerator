from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseForbidden
from django.template import RequestContext

from oppgavegen.generation_folder.generation import generate_level
from oppgavegen.view_logic.rating import *
from oppgavegen.view_logic.progress import *
from oppgavegen.models import Set, Chapter, Level
from oppgavegen.forms import QuestionForm
from oppgavegen.view_logic.submit_and_answer import *


@login_required
def game(request, set_id):
    context = RequestContext(request)
    set = Set.objects.get(pk=set_id)
    set_title = set.name
    if request.user in set.users.all():
        goto = render_to_response('game/screen.html', {'set_id': set_id, 'set_title': set_title}, context)
    else:
        goto = render_to_response('game/set_notmember.html', {'set': set}, context)
    return goto


def chapters(request, set_id):
    game_set = Set.objects.get(pk=set_id)
    set_title = game_set.name
    is_requirement = game_set.is_requirement
    is_password_protected = game_set.password_protected
    set_chapters = game_set.chapters.all()
    context = RequestContext(request)
    medals = [] # Both lists get updated in chapter_progress
    completed = []
    if is_requirement:
        # In case we want to do something special if the set is a requirement type set
        progress_number = chapter_progress(request.user, game_set, medals, completed)
    else:
        progress_number = chapter_progress(request.user, game_set, medals, completed)
    order = game_set.order
    set_chapters_ordered = []

    for x in order.split(','):
        for chapter in set_chapters:
            if chapter.pk == int(x):
                set_chapters_ordered.append(chapter)
                break
    if request.is_ajax():
        response = render_to_response('game/chapters.html',
                                  {'chapters': set_chapters_ordered, 'medals': json.dumps(medals),
                                   'completed': json.dumps(completed), 'progress_number': progress_number,
                                   'set_id': set_id, 'is_requirement': is_requirement,
                                   'is_password_protected': is_password_protected}, context)
    else:
        response = render_to_response('game/chapters_noajax.html',
                                  {'chapters': set_chapters_ordered, 'medals': json.dumps(medals),
                                   'completed': json.dumps(completed), 'progress_number': progress_number,
                                   'set_id': set_id, "set_title": set_title, "is_requirement": is_requirement,
                                   'is_password_protected': is_password_protected}, context)
    return response


def levels(request, chapter_id):
    game_chapter = Chapter.objects.get(pk=chapter_id)
    in_requirement_set = game_chapter.in_requirement_set
    chapter_levels = game_chapter.levels.all()
    chapter_title = game_chapter.name
    context = RequestContext(request)
    if in_requirement_set:
        progress_number = len(chapter_levels)
    else:
        progress_number = calculate_progress(request.user, game_chapter)
    star_per_level = get_stars_per_level(request.user, game_chapter)

    order = game_chapter.order
    chapter_levels_ordered = []

    for x in order.split(','):
        for chapter in chapter_levels:
            if chapter.pk == int(x):
                chapter_levels_ordered.append(chapter)
                break
    if request.is_ajax():
        return render_to_response('game/levels.html',
                                  {'levels': chapter_levels_ordered, 'chapter_title': chapter_title,
                                   'progress_number': progress_number, 'spl': star_per_level, 'chapter_id': chapter_id,
                                   'in_requirement_set':in_requirement_set},
                                  context)
    else:
        return render_to_response('game/levels_noajax.html',
                                  {'levels': chapter_levels_ordered, 'chapter_title': chapter_title,
                                   'progress_number': progress_number, 'spl': star_per_level, 'chapter_id': chapter_id,
                                   'in_requirement_set':in_requirement_set},
                                  context)

@login_required
def get_template(request):
    """Gets a template for a given level"""

    context = RequestContext(request)

    #if request.method == 'POST':
    context_dict = {'message': 'Noe har gått feil.'}
    form = request.POST
    if int(form.get('level_id')) == None:
        return redirect('/')
    level_id = int(form.get('level_id'))
    chapter_id = int(form.get('chapter_id'))
    set_id = int(form.get('set_id'))
    set = Set.objects.get(pk=set_id)
    #if check_for_level_skip(request.user, Chapter.objects.get(pk=chapter_id), level_id):
    #    return render_to_response('game/template.html', context_dict, context)
    context['set_title'] = set.name
    context['set_id'] = set_id
    context['chapter_id'] = chapter_id
    context['chapter_title'] = Chapter.objects.get(pk=chapter_id).name
    context['level_title'] = Level.objects.get(pk=level_id).name
    context['level_id'] = level_id
    context_dict = generate_level(request.user, level_id)
    context_dict['rating'] = get_user_rating(request.user)
    level = Level.objects.get(pk=level_id)
    context_dict['stars'] = get_user_stars_for_level(request.user, level)
    context_dict['ulp'] = get_user_rating_for_level(request.user, level)
    if request.is_ajax():
        return render_to_response('game/template.html', context_dict, context)
    else:
        return render_to_response('game/template_noajax.html', context_dict, context)




def get_solution(request, level=1):
    """Returns a render of answers.html"""
    context = RequestContext(request)
    cheat_message = '\\text{Ulovlig tegn har blitt brukt i svar}'
    required_message = '\\text{Svaret ditt har ikke utfylt alle krav}'
    render_to = 'game/answer.html'


    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            template = Template.objects.get(pk=form_values['primary_key'])

            user_answer = form_values['user_answer']
            try:
                disallowed = json.loads(template.disallowed)
            except ValueError:
                disallowed = []

            try:
                required = json.loads(template.required)
            except ValueError:
                required = []


            context_dict = make_answer_context_dict(form_values)

            if (cheat_check(user_answer, disallowed, form_values['variable_dictionary'].split('§'))) and\
                    (form_values['template_type'] == 'normal') and (context_dict['user_won']):
                context_dict['answer'] = cheat_message
                return render_to_response(render_to, context_dict, context)
            elif (required_check(user_answer, required, form_values['variable_dictionary'].split('§'))) and \
                    (form_values['template_type'] == 'normal') and (context_dict['user_won']):
                context_dict['answer'] = required_message
                return render_to_response(render_to, context_dict, context)


            if request.is_ajax():
                new_user_rating, new_star = change_level_rating(template, request.user, context_dict['user_won'],
                                                                form_values['template_type'], level)
                context_dict['chapter_id'] = request.POST['chapter_id']
                context_dict['ulp'] = int(new_user_rating)
                context_dict['new_star'] = new_star
                context_dict['stars'] = get_user_stars_for_level(request.user, Level.objects.get(pk=level))
                return render_to_response(render_to, context_dict, context)
            else:
                change_elo(template, request.user, context_dict['user_won'], form_values['template_type'])
            render_to_response(render_to, context_dict, context)
        else:
            print(form.errors)
