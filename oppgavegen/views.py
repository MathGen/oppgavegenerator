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

# Create your views here.

def index(request):
    #template = loader.get_template('index.html')
    context = RequestContext(request)
    arr = generation.pypartest()
    answer = str(arr[1])
    question = arr[0]
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            user_answer = form_values[0]
            answer = form_values[1]

            answer_text = generation.checkAnswer(user_answer,answer)
            context_dict = {'title': "spaghetti", 'question' : question, 'answer' : answer_text, 'user_answer' : user_answer}
            return render_to_response('answers', context_dict, context)
    else:
       form = QuestionForm()
       form.fields["answer"].initial = answer #Setter initsiell verdi til skjult felt i form.

    context_dict = {'title': generation.printer(), 'question' : question, 'answer' : str(answer), 'form' : form}
    return render_to_response('index', context_dict, context)


class QuestionForm(forms.Form):
    question = forms.CharField(label='', max_length=100)
    answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=100)

    def process(self):
        cd =  [self.cleaned_data['question'], self.cleaned_data['answer']]
        return cd

def playground(request):
    context = RequestContext(request)
    return render_to_response('playground', context)
