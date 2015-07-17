from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django_tables2 import RequestConfig
from selectable.decorators import login_required
from oppgavegen.templatetags.app_filters import is_teacher

@login_required
@user_passes_test(is_teacher, '/')
def templates(request):
    """Returns a render of tableview.html with all the templates"""
    panel_title = "Alle Maler"
    table = TemplateTable(Template.objects.filter(valid_flag=True))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})