from django.conf.urls import patterns, url
from ajaxsearch.views import *

urlpatterns = patterns('',
 url(r'^$', index, name='search_index'),
 url(r'^templates/$', ajax_template_search, name='ajax_template_search'),
                       )