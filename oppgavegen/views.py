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
    context_dict = {'title': "spaghetti", 'question' : question, 'answer' : str(answer)}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('Index', context_dict, context)

def answers(request):
    context = RequestContext(request)
    context_dict = {'title': "spaghetti"}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/answers/', context_dict, context)

    return render_to_response('answers', context_dict, context)

class QuestionForm(forms.Form):
    question = forms.CharField(label='question', max_length=100)