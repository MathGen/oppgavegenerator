from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseForbidden
from django.template import RequestContext

from oppgavegen.generation_folder.generation import generate_level
from oppgavegen.view_logic.rating import *
from oppgavegen.view_logic.progress import *
from oppgavegen.models import Set, Chapter, Level


@login_required
def game(request, set_id):
    context = RequestContext(request)
    set_title = Set.objects.get(pk=set_id).name
    return render_to_response('game/screen.html', {'set_id': set_id, 'set_title': set_title}, context)


def chapters(request, set_id):
    if request.is_ajax():
        game_set = Set.objects.get(pk=set_id)
        is_requirement = game_set.is_requirement
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

        return render_to_response('game/chapters.html',
                                  {'chapters': set_chapters_ordered, 'medals': json.dumps(medals),
                                   'completed': json.dumps(completed), 'progress_number': progress_number,
                                   'set_id': set_id, "is_requirement": is_requirement}, context)
    else:
        return HttpResponseForbidden()


def levels(request, chapter_id):

    if request.is_ajax():
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

        return render_to_response('game/levels.html',
                                  {'levels': chapter_levels_ordered, 'chapter_title': chapter_title,
                                   'progress_number': progress_number, 'spl': star_per_level, 'chapter_id': chapter_id,
                                   'in_requirement_set':in_requirement_set},
                                  context)
    else:
        return HttpResponseForbidden()

@login_required
def get_template(request):
    """Gets a template for a given level"""
    # if request.is_ajax():
    #   if request.method == 'GET':
    try:
        context = RequestContext(request)
        context_dict = {'message': 'Noe har gått feil.'}
        if request.method == 'POST':
            form = request.POST
            level_id = int(form['level_id[]'])
            chapter_id = int(form['chapter_id'])
            #if check_for_level_skip(request.user, Chapter.objects.get(pk=chapter_id), level_id):
            #    return render_to_response('game/template.html', context_dict, context)
            context_dict = generate_level(request.user, level_id)
            context_dict['rating'] = get_user_rating(request.user)
            level = Level.objects.get(pk=level_id)
            context_dict['stars'] = get_user_stars_for_level(request.user, level)
            context_dict['ulp'] = get_user_rating_for_level(request.user, level)

        return render_to_response('game/template.html', context_dict, context)
    except Exception as e:
        print(e)