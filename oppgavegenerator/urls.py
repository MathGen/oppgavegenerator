from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'oppgavegen.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/', 'oppgavegen.views.index', name='index'),
    url(r'^answers/', 'oppgavegen.views.answers', name='answers'),
    url(r'^templates/', 'oppgavegen.views.templates', name='templates'),
    url(r'^newtemplate/', 'oppgavegen.views.new_template', name='newtemplate'),
    url(r'^gen/', 'oppgavegen.views.gen', name='gen'),
    url(r'^submit/', 'oppgavegen.views.submit', name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^task/$', 'oppgavegen.views.index'),
    url(r"^task/(\d+)/$", 'oppgavegen.views.task_by_id'),
    url(r"^task/(\d+)/(\w+)/$", 'oppgavegen.views.task_by_id_and_type'),
    #url(r'^task/(?P<template_id>\d+)/(?P<desired_type>\d)/$', 'oppgavegen.views.task')



)
