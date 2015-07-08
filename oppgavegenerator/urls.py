"""

Configures how urls for the site works

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from oppgavegen.views.views import *
from oppgavegen.forms import *
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView
from oppgavegen.views.add_remove_views import *


urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^answers/', answers, name='answers'),
    url(r'^templates/$', templates, name='templates'),
    url(r'^newtemplate/', new_template, name='newtemplate'),
    url(r'^submit/', 'oppgavegen.views.views.submit', name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/templates/', 'oppgavegen.views.views.template_table_by_user', name='user_templates'),
    url(r'^task/$', 'oppgavegen.views.views.task'),
    url(r"^task/([\w ]+)/$", 'oppgavegen.views.views.task_by_extra', name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", 'oppgavegen.views.views.task_by_id_and_type', name='task_by_id_and_type'),
    url(r"^edit/(\d+)/$", 'oppgavegen.views.views.edit_template', name='edit_template'),
    url(r'^useranalysis/', 'oppgavegen.views.views.user_overview_table', name='user_table'),

    # Game
    url(r'^game/(\d+)/$', 'oppgavegen.views.views.game', name='game'),
    url(r'^game/(\d+)/levels/$', 'oppgavegen.views.views.levels', name='levels'),
    url(r'^game/(\d+)/chapters/$', 'oppgavegen.views.views.chapters', name='chapters'),
    url(r'^game/template/$', get_template, name='get_template'),
    url(r'^game/(\d+)/answer/$', 'oppgavegen.views.views.answers', name='get_answer'),

    # Sets, chapters and level management urls
    url(r'^user/sets/current/$', UserCurrentSetsEdit.as_view() , name='edit_current_user_sets' ),
    url(r'^set/new/$', 'oppgavegen.views.views.set_edit', name='add_new_set'),
    url(r'^set/(\d+)/edit/', set_edit, name='edit_set'),
    url(r'^chapter/new/$', 'oppgavegen.views.views.chapter_edit', name='add_new_chapter'),
    url(r'^chapter/(\d+)/edit', chapter_edit, name='edit_chapter'),
    url(r'^level/new/$', 'oppgavegen.views.views.level_edit', name='add_new_level'),
    url(r'^level/(\d+)/edit/', 'oppgavegen.views.views.level_edit', name='edit_level'),
    url(r'^level/(\d+)/stats/', level_stats, name='level_stats'),

    url(r'^set/(\d+)/$', set_detail_view, name='set_detail'),
    url(r'^set/(\d+)/chapters/$', SetChapterListView.as_view(), name='chapters_by_set'),
    url(r'^chapter/(\d+)/levels/$', ChapterLevelsListView.as_view(), name='levels_by_chapter'),
    url(r'^level/(\d+)/templates/$', LevelsTemplatesListView.as_view(), name='templates_by_level'),

    # Messy haystack search urls. Should maybe put these in own file and import here.
    # Search all content
   url(r'^search/$', include('haystack.urls')),
   # Search templates
   url(r'^templates/search/$', search_view_factory(
       template='search/template_search.html',
       searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template'),
       form_class=TemplateSearchForm,
       results_per_page=20 #default
       ), name='template_search'),

    # Mini search views (for jquery.load-situations)
    url(r'^minisearch/chapters/$', SearchView(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.chapter'),
        )),
   url(r'^minisearch/levels/$', SearchView(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.level'),
        )),
    url(r'^minisearch/templates/$', SearchView(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template'),
        )),

    # Search in sets, chapters or levels

    # url(r'^sets/search/$', SetSearch(
    #    template='search/search.html',
    #    searchqueryset=SearchQuerySet().models(Set),
    #    form_class=SetsSearchForm
    #    ), name='set_search'),
    # url(r'^chapters/search/$', SearchView(
    #     template='search/search.html',
    #     searchqueryset=SearchQuerySet().models(Chapter),
    #     form_class=SetsSearchForm
    # ), name='chapter_search'),
    # url(r'^levels/search/$', LevelSearch(
    #     #template='search/search.html',
    #     searchqueryset=SearchQuerySet().models(Level),
    #     form_class=SetsSearchForm,
    # ), name='level_search'),



    # AJAX FUNCTION URLS
    url(r'ajax/currentsets/refresh/$', refresh_navbar, name='refresh_navbar' ),


    # Return template preview html
    url(r'^template/([\w ]+)/preview/$', 'oppgavegen.views.views.preview_template', name='preview_template'),
    # Toggle template/level relationship for users current level
    url(r'^user/level/template/(\d+)/toggle/$', toggle_template_level, name='current_level_toggle'),
    url(r'^user/level/template/(\d+)/add/$', add_template_to_current_level, name='current_level_add'),
    url(r'^user/level/template/(\d+)/remove/$', remove_template_from_current_level, name='current_level_remove'),

    # Urls for sets, chapters and levels.
    url(r'^set/$', set_list, name='set'),  # A list over sets and the possibility of adding or edditing them.
    url(r'^set/(\d+)/([\w ]+)/new_chapter/$', new_chapter_for_set, name='new_chapter_for_set'),
    url(r'^set/(\d+)/chapter/(\d+)/add_chapter/$', add_chapter_to_set, name='add_chapter_to_set'),
    url(r'^set/(\d+)/chapter/(\d+)/remove_chapter/$', remove_chapter_from_set_view, name='remove_chapter_from_set'),
    url(r'^chapter/(\d+)/([\w ]+)/new_level/$', new_level_for_chapter, name='new_level_for_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/add_level/$', add_level_to_chapter, name='add_level_to_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/remove_level/$', remove_level_from_chapter_view, name='remove_level_from_chapter'),
    url(r'^level/(\d+)/template/(\d+)/add_template/$', add_template_to_level_view, name='new_chapter_for_set'),
    url(r'^level/(\d+)/template/(\d+)/remove_template/$', remove_template_from_level_view, name='remove_template_from_level'),

    url(r'^set/update/$', update_set_view, name='update_set_view'),
    url(r'^chapter/update/$', update_chapter_view, name='update_chapter_view'),
    url(r'^level/update/$', update_level_view, name='update_level_view'),

    # DJANGO SELECTABLE
    # Might be useful for autocomplete for tagging
    # Meant to work with jquery ui https://github.com/mlavin/django-selectable
    url(r'^selectable/', include('selectable.urls')),
)
