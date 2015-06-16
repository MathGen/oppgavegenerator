"""

Configures how urls for the site works

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from oppgavegen.views import *
from oppgavegen.forms import *
from haystack.forms import SearchForm
import datetime
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.views.generic import ListView

sqs = SearchQuerySet().filter(creation_date__lte=datetime.datetime.now())

urlpatterns = patterns('',
    url(r'^$', 'oppgavegen.views.index', name='home'),
    url(r'^answers/', 'oppgavegen.views.answers', name='answers'),
    url(r'^templates/', 'oppgavegen.views.templates', name='templates'),
    url(r'^newtemplate/', 'oppgavegen.views.new_template', name='newtemplate'),
    url(r'^gen/', 'oppgavegen.views.gen', name='gen'),
    url(r'^submit/', 'oppgavegen.views.submit', name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/templates/', 'oppgavegen.views.template_table_by_user', name='user_templates'),
    url(r'^user/sets/', UserSetListView.as_view(), name='user_sets'),
    url(r'^task/$', 'oppgavegen.views.task'),
    url(r"^task/([\w ]+)/$", 'oppgavegen.views.task_by_extra', name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", 'oppgavegen.views.task_by_id_and_type', name='task_by_id_and_type'),
    url(r"^edit/(\d+)/$", 'oppgavegen.views.edit_template', name='edit_template'),
    url(r'^useranalysis/', 'oppgavegen.views.user_overview_table', name='user_table'),

    # Sets, chapters and level management urls
    url(r'^set/new/', SetCreateView.as_view(), name='set_create_new'),
    url(r'^set/(\d+)/chapters/edit/$', 'oppgavegen.views.manage_chapters_in_set', name='manage_chapters_in_set'),
    url(r'^set/(\d+)/chapters/$', SetChapterListView.as_view(), name='chapters_by_set'),
    url(r'^chapter/new/', 'oppgavegen.views.manage_chapters', name='manage_chapters' ),
    url(r'^chapter/(\d+)/levels/$', ChapterLevelsListView.as_view(), name='levels_by_chapter'),
    url(r'^level/new/', CreateView.as_view(form_class=LevelCreateForm, template_name='sets/level_create_form.html'), name='level_create',),
    url(r'^level/(\d+)/templates/$', LevelsTemplatesListView.as_view(), name='templates_by_level'),

    # Messy haystack search urls. Could put these in own file and import here.
    url(r'^search/', include('haystack.urls')),
    url(r'^search/templates/$', SearchView(
        template='search/template_search.html',
        searchqueryset=sqs,
        form_class=TemplateSearchForm
    ), name='template_search'),


    # AJAX FUNCTION URLS
    # Return template preview html
    url(r'^template/([\w ]+)/preview/$', 'oppgavegen.views.preview_template', name='preview_template'),
    # Add level to template
    url(r'^level/(\d+)/template/(\d+)/add/$', 'oppgavegen.views.level_add_template', name='level_add_template' ),

    # DJANGO SELECTABLE
    url(r'^selectable/', include('selectable.urls')),

    # Experimental ajax search functions
    url(r'ajax/search/', include('ajaxsearch.urls')),
)
