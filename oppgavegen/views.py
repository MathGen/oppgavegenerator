from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from random import randint
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from oppgavegen import generation
#sympy
from sympy import sympify
from sympy.printing.mathml import mathml
from sympy import Integral, latex
from django.forms import ModelForm
# models and tables
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import User
from oppgavegen.tables import *
from django_tables2 import RequestConfig
from datetime import datetime
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen import view_logic

def is_member(user): #Checks if a user is a member of a group
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()


@login_required
def index(request):
    #template = loader.get_template('index.html')
    context = RequestContext(request)
    question_type = request.GET.get('q', '')
    if question_type != "":
        context_dict = generation.task_with_solution(question_type)
    else:
        context_dict = generation.task_with_solution("")
    context_dict['title'] = generation.printer()
    return render_to_response('index', context_dict, context)

@login_required
def task_by_id_and_type(request, template_id, desired_type='normal'):
    context = RequestContext(request)
    context_dict = generation.task_with_solution(template_id, desired_type)
    context_dict['title'] = generation.printer()

    return render_to_response('index', context_dict, context)

@login_required
def task_by_id(request, template_id):
    context = RequestContext(request)
    context_dict = generation.task_with_solution(template_id)
    context_dict['title'] = generation.printer()
    return render_to_response('index', context_dict, context)


class QuestionForm(forms.Form):
    user_answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    primary_key = forms.IntegerField()
    variable_dictionary = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    template_specific = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    template_type = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=20)

    def process(self):
        cd = {'variable_dictionary' : self.cleaned_data['variable_dictionary'],'primary_key' : self.cleaned_data['primary_key'],
              'user_answer' : self.cleaned_data['user_answer'], 'template_type' : self.cleaned_data['template_type'],
              'template_specific' : self.cleaned_data['template_specific']}
        return cd

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__' #['question_text', 'solution', 'answer', 'variables','number_of_decimals','answer_can_be_zero','random_domain'] #todo add creator..

        def process(self):
            cd =  [self.cleaned_data['question'], self.cleaned_data['answer']]
            return cd

@login_required
@user_passes_test(is_teacher, '/')
def gen(request):
    context = RequestContext(request)
    #retrieves a list of topics and passes them to the view.
    topics = ""
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics':topics}
    return render_to_response('gen.html', context_dict, context)

@login_required
@user_passes_test(is_teacher, '/')
def submit(request):
    message = 'don\'t come here'
    if request.method == 'POST':
        message = 'failure!'
        #todo check input for errors
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)

            template.creator = request.user
            #could get creator from username=einar as well
            template.rating = 1200
            template.times_failed = 0
            template.times_solved = 0
            template.creation_date = datetime.now()
            template.save()

            message = 'success!'
        else:
            print(form.errors)
    context = RequestContext(request)
    return render_to_response('submit',{'message': message}, context)

@login_required
def answers(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        counter = 0
        if form.is_valid():
            form_values = form.process()
            #print(form_values)
            context_dict = view_logic.make_answer_context_dict(form_values)
            return render_to_response('answers', context_dict, context)
        else:
            print(form.errors)
    return  render_to_response('answers')

@login_required
@user_passes_test(is_teacher, '/')
def templates(request):
    panel_title = "Alle Maler"
    table = BootstrapTemplateTable(Template.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "templates.html", {"table": table, "panel_title": panel_title})

@login_required
@user_passes_test(is_teacher, '/')
def template_table_by_user(request):
    user = request.user
    panel_title = "Dine Maler"
    table = UserTemplates(Template.objects.filter(creator=user))
    RequestConfig(request).configure(table)
    return render(request, "templates.html", {"table": table, "panel_title": panel_title})

@login_required
@user_passes_test(is_teacher, '/')
def new_template(request):
    context = RequestContext(request)
    #retrieves a list of topics and passes them to the view.
    topics = ""
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics':topics}
    return render_to_response('newtemplate.html', context_dict, context)


def edit_template(request, template_id):
    context = RequestContext(request)
    context_dict = view_logic.make_edit_context_dict(template_id)
    return render_to_response('edit.html', context_dict, context)

def update_template(request):
    context = RequestContext(request)
    context_dict = {'msg','success'}


    return render_to_response('update.html', context_dict, context)
