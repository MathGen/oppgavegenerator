from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen.view_logic.statistics import stats_for_set
from oppgavegen.models import Set, Chapter, Level, Template
from django.contrib.auth.decorators import login_required, user_passes_test

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