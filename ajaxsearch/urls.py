from django.conf.urls import patterns, url
from ajaxsearch.views import *

urlpatterns = patterns('',
 url(r'^$', index, name='search_index'),
 url(r'^templatessearchajax/$', ajax_template_search, name='ajax_template_search'),
 url(r'^templates/(?P<query>[\w]+)/$', ajax_template_search_test, name='ajax_template_search'),)