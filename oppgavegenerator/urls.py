"""

Configures how urls for the site works

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from oppgavegen.views.views import *
from oppgavegen.forms import *
from oppgavegen.views.views import SetSearch#, ChapterSearch, LevelSearch, SetsSearchView
from haystack.forms import SearchForm
import datetime
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from haystack.views import SearchView
from django.views.generic import ListView, CreateView

urlpatterns = patterns('',
    url(r'^$', 'oppgavegen.views.views.index', name='home'),
    url(r'^answers/', 'oppgavegen.views.views.answers', name='answers'),
    url(r'^templates/$', 'oppgavegen.views.views.templates', name='templates'),
    url(r'^newtemplate/', 'oppgavegen.views.views.new_template', name='newtemplate'),
    url(r'^gen/', 'oppgavegen.views.views.gen', name='gen'),
    url(r'^submit/', 'oppgavegen.views.views.submit', name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/templates/', 'oppgavegen.views.views.template_table_by_user', name='user_templates'),
    url(r'^user/sets/$', UserSetListView.as_view(), name='user_sets'),
    url(r'^task/$', 'oppgavegen.views.views.task'),
    url(r"^task/([\w ]+)/$", 'oppgavegen.views.views.task_by_extra', name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", 'oppgavegen.views.views.task_by_id_and_type', name='task_by_id_and_type'),
    url(r"^edit/(\d+)/$", 'oppgavegen.views.views.edit_template', name='edit_template'),
    url(r'^useranalysis/', 'oppgavegen.views.views.user_overview_table', name='user_table'),

    # Sets, chapters and level management urls
    url(r'^game/(\d+)/$', 'oppgavegen.views.views.game', name='game'),
    url(r'^game/(\d+)/levels/$', 'oppgavegen.views.views.levels', name='levels'),
    url(r'^game/(\d+)/chapters/$', 'oppgavegen.views.views.chapters', name='chapters'),
    url(r'^game/(\d+)/template/$', 'oppgavegen.views.views.get_template', name='get_template'),
    url(r'^game/(\d+)/answer/$', 'oppgavegen.views.views.answers', name='get_answer'),
    url(r'^user/sets/current/$', UserCurrentSetsEdit.as_view() , name='edit_current_user_sets' ),
    url(r'^set/new/', SetCreateView.as_view(), name='set_create_new'),
    url(r'^set/(\d+)/$', set_detail_view, name='set_detail'),
    url(r'^set/(\d+)/chapters/edit/$', 'oppgavegen.views.views.manage_chapters_in_set', name='manage_chapters_in_set'),
    url(r'^set/(\d+)/chapters/$', SetChapterListView.as_view(), name='chapters_by_set'),
    url(r'^chapter/new/', 'oppgavegen.views.views.manage_chapters', name='manage_chapters' ),
    url(r'^chapter/(\d+)/levels/$', ChapterLevelsListView.as_view(), name='levels_by_chapter'),
    url(r'^level/new/', CreateView.as_view(form_class=LevelCreateForm, template_name='sets/level_create_form.html'), name='level_create',),
    url(r'^level/(\d+)/templates/$', LevelsTemplatesListView.as_view(), name='templates_by_level'),

    # Messy haystack search urls. Should maybe put these in own file and import here.
    # Search all content
    url(r'^search/$', include('haystack.urls')),
    # Search templates
    url(r'^templates/search/$', SearchView(
        template='search/template_search.html',
        searchqueryset=SearchQuerySet().models(Template),
        form_class=TemplateSearchForm
    ), name='template_search'),
    # Search in sets, chapters or levels

    #url(r'^sets/search/$', SetSearch(
        #template='search/search.html',
    #    searchqueryset=SearchQuerySet().models(Set),
    #    form_class=SetsSearchForm
    #), name='set_search'),
    # url(r'^chapters/search/$', SearchView(
    #     #template='search/search.html',
    #     searchqueryset=SearchQuerySet().models(Chapter),
    #     form_class=SetsSearchForm
    # ), name='chapter_search'),
    # url(r'^levels/search/$', LevelSearch(
    #     #template='search/search.html',
    #     searchqueryset=SearchQuerySet().models(Level),
    #     form_class=SetsSearchForm,
    # ), name='level_search'),



    # AJAX FUNCTION URLS
    # Return template preview html
    url(r'^template/([\w ]+)/preview/$', 'oppgavegen.views.preview_template', name='preview_template'),
    # Add template to a spesific level ( i.e:  /level/[level id]/template/[template id]/add )
    url(r'^level/(\d+)/template/(\d+)/add/$', 'oppgavegen.views.level_add_template', name='level_add_template' ),
    # Add / remove template to current user level
    url(r'^user/level/template/(\d+)/add/$', add_template_to_current_level, name='current_level_add'),
    url(r'^user/level/template/(\d+)/remove/$', remove_template_from_current_level, name='current_level_remove'),

    # DJANGO SELECTABLE
    url(r'^selectable/', include('selectable.urls')),

    # Experimental ajax search functions
    url(r'ajax/search/', include('ajaxsearch.urls')),
)
