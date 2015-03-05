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
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import User
from datetime import datetime
from oppgavegen.templatetags.app_filters import is_teacher

def is_member(user): #Checks if a user is a member of a group
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()


@login_required
def index(request):
    #template = loader.get_template('index.html')
    context = RequestContext(request)
    question_type = request.GET.get('q', '')
    if question_type == "algebra":
        arr = generation.algebra()
    elif question_type == "aritmetikk":
        arr = generation.arithmetics()
    else:
        arr = generation.task_with_solution()

    question = arr[0]
    primary_key = arr[4]
    variable_dictionary = arr[1]
    choices = str(arr[3])
    number_of_answers = arr[5]
    print(choices)
    template_type = arr[2]
    context_dict = {'title': generation.printer(), 'question' : question,  'choices' : choices, 'template_type' : template_type, 'primary_key' : primary_key,
                    'variable_dictionary' : variable_dictionary, 'number_of_answers' : number_of_answers}
    return render_to_response('index', context_dict, context)


class QuestionForm(forms.Form):
    user_answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    primary_key = forms.IntegerField()
    variable_dictionary = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)

    def process(self):
        cd =  [self.cleaned_data['user_answer'], self.cleaned_data['primary_key'], self.cleaned_data['variable_dictionary']]
        return cd

def playground(request):
    context = RequestContext(request)
    return render_to_response('playground', context)

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__' #['question_text', 'solution', 'answer', 'variables','number_of_decimals','answer_can_be_zero','random_domain'] #todo add creator..

        def process(self):
            cd =  [self.cleaned_data['question'], self.cleaned_data['answer']]
            return cd

def test(request):
    context = RequestContext(request)
    return render_to_response('test.html', context)

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
            template.choices = ""
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
            user_answer = form_values[0]
            print(form_values)
            q = Template.objects.get(pk=form_values[1])
            variable_dictionary = form_values[2].split('§')
            print(variable_dictionary)
            print(q.answer)
            answer = generation.replace_variables_from_array(variable_dictionary, q.answer)
            print(answer)
            answer = generation.parse_answer(answer)
            answer = answer.replace('`','')

            solution = generation.replace_variables_from_array(variable_dictionary, q.solution)
            solution = generation.parse_solution(solution)

            user_answer = user_answer.split('§') #if a string doesn't contain the split character it returns as a list with 1 element
            answer = answer.split('§')
            #We format both the user answer and the answer the same way.
            user_answer = [ generation.after_equal_sign(x) for x in user_answer ]
            answer = [ generation.after_equal_sign(x) for x in answer ]
            user_answer = generation.calculate_array(user_answer)
            answer = generation.calculate_array(answer)

            answer_text = generation.checkAnswer(user_answer,answer)
            context_dict = {'title': "Oppgavegen",  'answer' :  str(answer_text), 'user_answer' : user_answer, 'solution' : solution}
            return render_to_response('answers', context_dict, context)
        else:
            print(form.errors)
    return  render_to_response('answers')

