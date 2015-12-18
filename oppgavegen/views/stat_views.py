from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from oppgavegen.view_logic.statistics import *
from oppgavegen.models import Set, Level, UserLevelProgress


@login_required
def set_stats_view(request, set_id):
    """Returns a render of statview.html with all the templates"""
    # todo: clickable chapter names with link to in depth chapter stats
    set = Set.objects.get(pk=set_id)
    if set.is_requirement and set.editor == request.user:
        headers, user_stats = stats_for_set(int(set_id))
        print(headers)
        print(user_stats)
        return render(request, 'statview.html', {'headers': headers, 'user_stats': user_stats,
                                             'panel_title': 'Arbeidskravstatistikk for sett' + ' - ' + set.name})
    else:
        return redirect('index')

@login_required
def detailed_chapter_stats(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    if chapter.in_requirement_set and chapter.editor == request.user:
        headers, user_stats = stats_for_chapter_levels(chapter_id)

        return render(request, "statview_levels.html", {"headers": headers, "user_stats": user_stats,
                                                        'panel_title': 'Arbeidskravstistikk for kapittel' + ' - ' +
                                                        chapter.name})

    else:
        return redirect('index')


@login_required
def level_stats(request, level_id):
    """
    Prepares rating statistics for a level by counting student level/template ratings within specific intervals.
    Designed with morris.js bar chart in mind (see charts.html)
    The range is from 0 to 2400, and the measuring interval is 100 counting from 1100 and up.
    """

    context_dict = {}
    level = Level.objects.get(pk=level_id)
    context_dict['level_name'] = level.name
    stats = level.student_progresses.all()

    offset = level.offset
    student_ratings = stats.values_list('level_rating', flat=True) # list of all ratings

    if student_ratings:
        context_dict['players'] = len(student_ratings)
        context_dict['average'] = int(sum(student_ratings)/context_dict['players'])

    context_dict['levelid'] = level_id
    context_dict['user_is_owner'] = (level.editor == request.user) # check if current user is level owner
    context_dict['offset'] = offset
    context_dict['student_entries'] = get_level_student_statistics(level)
    context_dict['templates'] = level.templates.exists()
    context_dict['template_entries'] = get_level_template_statistics(level, offset)
    context_dict['template_original'] = get_level_template_original_statistics(level)
    return render(request, 'sets/charts.html', context_dict)
