"""

Defines views, and renders data to html templates.

"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from oppgavegen.tables import *
from django_tables2 import RequestConfig
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen import view_logic
from oppgavegen.view_logic import *


def is_member(user):
    """Returns true/false depending on if the user is a member of the teacher group (or is a superuser)"""
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()


@login_required
def task(request):
    """Returns a render of taskview.html with a rating apropriate math question"""
    context = RequestContext(request)
    question_type = request.GET.get('q', '')
    if question_type != "":
        context_dict = generation.generate_task(request.user, question_type)
    else:
        context_dict = generation.generate_task(request.user, "")
    context_dict['rating'] = view_logic.get_user_rating(request.user)
    return render_to_response('taskview.html', context_dict, context)


@login_required
def task_by_id_and_type(request, template_extra, desired_type='normal'):
    """Returns a render of taskview with a specific math template with specified type"""
    context = RequestContext(request)
    context_dict = generation.generate_task(request.user, template_extra, desired_type)
    context_dict['rating'] = view_logic.get_user_rating(request.user)
    if context_dict['question'] == 'error':
        message = {'message': 'Denne oppgavetypen har ikke blitt laget for denne oppgaven'}
        return render_to_response('error.html', message, context)
    return render_to_response('taskview.html', context_dict, context)


@login_required
def task_by_extra(request, template_extra):
    """Returns a render of taskview with a specific math template"""
    context = RequestContext(request)
    context_dict = generation.generate_task(request.user, template_extra)
    context_dict['rating'] = view_logic.get_user_rating(request.user)
    return render_to_response('taskview.html', context_dict, context)


class QuestionForm(forms.Form):
    user_answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    primary_key = forms.IntegerField()
    variable_dictionary = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    template_specific = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    template_type = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=50)
    replacing_words = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    disallowed = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)

    def process(self):
        """Returns a cleaned dictionary of it's own values."""
        cd = {'variable_dictionary': self.cleaned_data['variable_dictionary'],
              'primary_key': self.cleaned_data['primary_key'],
              'user_answer': self.cleaned_data['user_answer'],
              'template_type': self.cleaned_data['template_type'],
              'template_specific': self.cleaned_data['template_specific'],
              'replacing_words': self.cleaned_data['replacing_words'],
              'disallowed': self.cleaned_data['disallowed']}
        return cd


class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__'

        def process(self):
            """Returns a cleaned dictionary of it's own values."""
            cd = {self.cleaned_data['question'], self.cleaned_data['answer']}
            return cd


@login_required
@user_passes_test(is_teacher, '/')
def gen(request):
    """Returns a render of gen.html"""
    context = RequestContext(request)
    topics = ""
    for e in Topic.objects.all():  # Retrieves a list of topics and passes them to the view.
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics': topics, 'rating': view_logic.get_user_rating(request.user)}
    return render_to_response('gen.html', context_dict, context)


@login_required
@user_passes_test(is_teacher, '/')
def submit(request):
    """Returns a render of submit html. Different depending on if the submission goes through ot not"""
    message = 'don\'t come here'
    if request.method == 'POST':
        message = 'Det har skjedd noe feil ved innsending av form'
        # todo check input for errors
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            if request.REQUEST['pk'] != '':  # Can this be written as v = req != ''?
                template.pk = request.REQUEST['pk']  # Workaround, template doesn't automatically get template.pk
                update = True
            else:
                update = False
            message = view_logic.submit_template(template, request.user, update)

        else:
            print(form.errors)
    context = RequestContext(request)
    return render_to_response('submit.html', {'message': message}, context)


@login_required
def answers(request):
    """Returns a render of answers.html"""
    context = RequestContext(request)
    cheat_message = '\\text{Ulovlig tegn har blitt brukt i svar}'
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            template = Template.objects.get(pk=form_values['primary_key'])
            if cheat_check(form_values['user_answer'], template.disallowed):
                return render_to_response('answers.html', {'answer': cheat_message}, context)
            context_dict = view_logic.make_answer_context_dict(form_values)
            view_logic.change_elo(template, request.user, context_dict['user_won'], form_values['template_type'])
            context_dict['rating'] = view_logic.get_user_rating(request.user)
            return render_to_response('answers.html', context_dict, context)
        else:
            print(form.errors)
    return render_to_response('answers.html')


@login_required
@user_passes_test(is_teacher, '/')
def templates(request):
    """Returns a render of tableview.html with all the templates"""
    panel_title = "Alle Maler"
    table = TemplateTable(Template.objects.filter(valid_flag=True))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def template_table_by_user(request):
    """Returns a render of tableview.html with only templates from the logged in user."""
    user = request.user
    panel_title = "Dine Maler"
    table = UserTemplatesTable(Template.objects.filter(creator=user))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def user_overview_table(request):
    """Returns a render of tableview.html with overview over users"""
    panel_title = "Brukere"
    table = UserTable(ExtendedUser.objects.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def new_template(request):
    """Returns a render of newtemplate.html used for creating new templates"""
    context = RequestContext(request)
    # Retrieves a list of topics and passes them to the view.
    topics = ""
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics': topics, 'rating': view_logic.get_user_rating(request.user)}
    return render_to_response('newtemplate.html', context_dict, context)


@login_required
@user_passes_test(is_teacher, '/')
def edit_template(request, template_id):
    """Returns a render of edit.html used for editing existing templates"""
    context = RequestContext(request)
    context_dict = view_logic.make_edit_context_dict(template_id)
    context_dict['rating'] = view_logic.get_user_rating(request.user)
    return render_to_response('edit.html', context_dict, context)


@login_required
def index(request):
    list = Topic.objects.values_list('topic', flat=True)

    return render(request, "index.html", {"list": list})

