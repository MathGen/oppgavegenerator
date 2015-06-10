from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from oppgavegen.models import Template
from oppgavegen.models import Topic
from django.contrib.auth.models import User
import time

def index(request):
    return render_to_response('search/ajaxsearch.html', {}, context_instance=RequestContext(request))

def ajax_template_search(request, ):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            results = Template.objects.filter(topic__topic__contains=q, valid_flag=True)
            return render_to_response('search/results.html', { 'results': results, },
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse("q is not None")
    else:
        return HttpResponse("Request is not AJAX")


# todo fix jquery code to match this ok
def ajax_template_search_test(request, query=None):
    # if request.is_ajax():
        if query is not None:
            results = Template.objects.filter(topic__topic__contains=query, valid_flag=True)
            return render_to_response('search/results.html', { 'results': results, },
                                      context_instance=RequestContext(request))
    # else:
        return HttpResponse("Request is not AJAX.")