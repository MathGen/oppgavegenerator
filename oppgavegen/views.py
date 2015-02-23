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
from sympy.abc import x
from django.forms import ModelForm
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import User
from datetime import datetime

# Create your views here.

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
    answer = str(arr[1])
    question = arr[0]
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            user_answer = form_values[0]
            print('Before:' + user_answer)
            user_answer = generation.calculateAnswer(user_answer) #format the userinput the same way we format the solution
            print('After:' + user_answer)
            answer = form_values[1]
            answer_text = generation.checkAnswer(user_answer,answer)
            context_dict = {'title': "Oppgavegen", 'question' : question, 'answer' :  str(answer_text), 'user_answer' : user_answer}
            #make a button on the answers page with "generate new question"
            return render_to_response('answers', context_dict, context)
    else:
       form = QuestionForm()
       form.fields["answer"].initial = answer #Setter initsiell verdi til skjult felt i form.
    choices = str(arr[3])
    print(choices)
    template_type = arr[2]
    #todo get type and choices in the template and generate a form with jquery acordingly
    context_dict = {'title': generation.printer(), 'question' : question, 'answer' : answer, 'form' : form, 'choices' : choices, 'template_type' : template_type}
    return render_to_response('index', context_dict, context)


class QuestionForm(forms.Form):
    user_answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)

    def process(self):
        cd =  [self.cleaned_data['user_answer'], self.cleaned_data['answer']]
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

def gen(request):
    context = RequestContext(request)
    return render_to_response('gen.html', context)

def submit(request):
    message = 'don\'t come here'
    if request.method == 'POST':
        message = 'failure!'
        #todo check input for errors
        form = TemplateForm(request.POST)
        print(form)
        if form.is_valid():
            template = form.save(commit=False)
            print(template.topic)
            print(template.topic_id)
            template.topic = Topic.objects.get(pk=7)
            template.creator = User.objects.get(pk=2) #todo get user from the user submitting the form
            #could get creator from username=einar
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

def answers(request):
    #todo: move logic from index post to here.
    context = RequestContext(request)
    if request.method == 'POST':
        print("honka_")
        form = QuestionForm(request.POST)
        if form.is_valid():
            print("dory")
            form_values = form.process()
            user_answer = form_values[0]
            print('Before:' + user_answer)
            user_answer = generation.calculateAnswer(user_answer) #format the userinput the same way we format the solution
            print('After:' + user_answer)
            answer = form_values[1]
            answer_text = generation.checkAnswer(user_answer,answer)
            context_dict = {'title': "Oppgavegen",  'answer' :  str(answer_text), 'user_answer' : user_answer}
            #todo make a button on the answers page with "generate new question"
            return render_to_response('answers', context_dict, context)
        else:
            print(form.errors)
    return  render_to_response('answers')
