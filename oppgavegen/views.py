from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from random import randint
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms


# Create your views here.

def index(request):
    #template = loader.get_template('index.html')
    context = RequestContext(request)
    number1 = randint(0,10)
    number2 = randint(0,10)
    operators = ["+", "-"]
    opNumber = randint(0,1)
    if opNumber == 0:
        answer = number1 + number2
    else:
        answer = number1 - number2

    question = "hva er " + str(number1) + " " + operators[opNumber] + " " + str(number2)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_values = form.process()
            user_answer = form_values[0]
            answer = form_values[1]

            # redirect to a new URL:
            context_dict = {'title': "spaghetti", 'question' : question, 'answer' : str(answer), 'user_answer' : user_answer}
            return render_to_response('answers', context_dict, context)
    else:
       form = QuestionForm()
       form.fields["answer"].initial = str(answer)


    context_dict = {'title': "spaghetti", 'question' : question, 'answer' : str(answer), 'form' : form}
    return render_to_response('Index', context_dict, context)

def answers(request, context_dict, cont):
    context = RequestContext(request)
    context = cont
    context_dict2 = context_dict



    return render_to_response('answers', context_dict, context)

class QuestionForm(forms.Form):
    question = forms.CharField(label='', max_length=100)
    answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=100)

    def process(self):
        cd =  [self.cleaned_data['question'], self.cleaned_data['answer']]
        return cd