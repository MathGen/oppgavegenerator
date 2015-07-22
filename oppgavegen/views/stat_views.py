from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django_tables2 import RequestConfig
from selectable.decorators import login_required
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen.view_logic.statistics import stats_for_set



def set_stats_view(request, set_id):
    """Returns a render of tableview.html with all the templates"""
    headers, user_stats = stats_for_set(int(set_id))
    print(headers)
    print(user_stats)
    return render(request, "statview.html", {"headers": headers, "user_stats": user_stats,
                                             'panel_title': 'Brukerstatistikk'})