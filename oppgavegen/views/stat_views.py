from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from oppgavegen.view_logic.statistics import *
from oppgavegen.models import Set, Level


@login_required
def set_stats_view(request, set_id):
    """Returns a render of statview.html with all the templates"""
    set = Set.objects.get(pk=set_id)
    if set.is_requirement and set.editor == request.user:
        headers, user_stats = stats_for_set(int(set_id))
        print(headers)
        print(user_stats)
        return render(request, "statview.html", {"headers": headers, "user_stats": user_stats,
                                             'panel_title': 'Brukerstatistikk'})
    else:
        return redirect('index')

@login_required
def level_stats(request, level_id):
    """
    Prepares rating statistics for a level by counting student level. / template-ratings within specific intervals.
    Designed with morris.js bar chart in mind (see charts.html)
    The range is from 0 to 2400, and the measuring interval is 100 counting from 1100 and up.
    """

    context_dict = {}
    level = Level.objects.get(pk=level_id)
    context_dict['level_name'] = level.name
    stats = level.student_progresses.all()

    studentratings = stats.values_list('level_rating', flat=True) # list of all ratings

    if studentratings:
        context_dict['players'] = len(studentratings)
        context_dict['average'] = int(sum(studentratings)/context_dict['players'])

    context_dict['student_entries'], context_dict['student_namestar'] = get_level_student_statistics(level)
    context_dict['templates'] = level.templates.exists()
    context_dict['template_entries'] = get_level_template_statistics(level)
    context_dict['template_original'] = get_level_template_original_statistics(level)
	
    return render(request, 'sets/charts.html', context_dict)
