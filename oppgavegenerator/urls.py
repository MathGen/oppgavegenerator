"""

Configures how urls for the site works

"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from oppgavegen.views.views import *
from oppgavegen.views.stat_views import *
from oppgavegen.forms import *
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
#from haystack.generic_views import SearchView
from registration.backends.default.views import RegistrationView
from oppgavegen.views.add_remove_views import *
from oppgavegen.view_logic.db_format import format_domain


urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^answers/', answers, name='answers'),
    url(r'^templates/$', TemplatesListView.as_view(), name='templates'),
    url(r'^newtemplate/', new_template, name='newtemplate'),
    url(r'^submit/', submit, name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/register/$', RegistrationView.as_view(form_class=NamedUserRegistrationForm), name='registration_register'),
    url(r'^user/settings/$', UserSettingsView.as_view(), name='user_settings'),
    url(r'^user/settings/deactivate/$', user_deactivate, name='user_deactivate'),
    url(r'^user/templates/$', UserTemplatesListView.as_view(), name='user_templates_list'),
    url(r'^task/$', task),
    url(r"^task/([\w ]+)/$", task_by_extra, name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", task_by_id_and_type, name='task_by_id_and_type'),
    url(r"^edit/(\d+)/$", edit_template, name='edit_template'),

    # Game
    url(r'^game/(\d+)/$', game, name='game'),
    url(r'^game/(\d+)/levels/$', levels, name='levels'),
    url(r'^game/(\d+)/chapters/$', chapters, name='chapters'),
    url(r'^game/template/$', get_template, name='get_template'),
    url(r'^game/(\d+)/answer/$', answers, name='get_answer'),

    # Sets, chapters and level management urls
    url(r'^user/sets/current/$', UserCurrentSetsEdit.as_view() , name='edit_current_user_sets' ),
    url(r'^set/new/$', set_edit, name='add_new_set'),
    url(r'^set/(\d+)/edit/', set_edit, name='edit_set'),
    url(r'^chapter/new/$', chapter_edit, name='add_new_chapter'),
    url(r'^chapter/(\d+)/edit', chapter_edit, name='edit_chapter'),
    url(r'^level/new/$', level_edit, name='add_new_level'),
    url(r'^level/(\d+)/edit/', level_edit, name='edit_level'),
    url(r'^level/(\d+)/stats/', level_stats, name='level_stats'),

    url(r'^set/(\d+)/$', set_detail_view, name='set_detail'),
    url(r'^set/(\d+)/chapters/$', SetChapterListView.as_view(), name='chapters_by_set'),
    url(r'^chapter/(\d+)/levels/$', ChapterLevelsListView.as_view(), name='levels_by_chapter'),
    url(r'^level/(\d+)/templates/$', LevelsTemplatesListView.as_view(), name='templates_by_level'),

    # Haystack search urls
    # Search all content
    url(r'^search/$', include('haystack.urls')),
   # Search templates
    url(r'^templates/search/$', search_view_factory(

        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template', copy=False),
        template='search/template_search.html',
        form_class=TemplateSearchForm,
    ), name='templates_search'),

    # Mini search views (for jquery.load-situations)
    url(r'^minisearch/chapters/$', search_view_factory(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.chapter', copy=False),
        )),
   url(r'^minisearch/levels/$', search_view_factory(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.level', copy=False),
        )),
    url(r'^minisearch/templates/$', search_view_factory(
        template='search/mini_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template', copy=False),
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


    # Return template as JSON
    url(r'^template/([\w ]+)/preview/$', preview_template, name='preview_template'),
    # Toggle template/level relationship for users current level
    #url(r'^user/level/template/(\d+)/toggle/$', toggle_template_level, name='current_level_toggle'),
    url(r'^user/level/template/(\d+)/toggle/$', toggle_template_level_membership, name='current_level_toggle'),
    url(r'^user/level/template/(\d+)/add/$', add_template_to_current_level, name='current_level_add'),
    url(r'^user/level/template/(\d+)/remove/$', remove_template_from_current_level, name='current_level_remove'),

    # Urls for sets, chapters and levels.
    url(r'^set/$', set_list, name='set'),  # A list over sets and the possibility of adding or edditing them.
    url(r'^set/([\w ]+)/new_set/$', new_set_view, name='new_set_view'),
    url(r'^set/(\d+)/remove_set/$', remove_set_view, name='remove_set_view'),
    url(r'^set/(\d+)/([\w ]+)/new_chapter/$', new_chapter_for_set, name='new_chapter_for_set'),
    url(r'^set/(\d+)/chapter/(\d+)/add_chapter/$', add_chapter_to_set_view, name='add_chapter_to_set'),
    url(r'^set/(\d+)/chapter/(\d+)/remove_chapter/$', remove_chapter_from_set_view, name='remove_chapter_from_set'),
    url(r'^chapter/(\d+)/([\w ]+)/new_level/$', new_level_for_chapter, name='new_level_for_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/add_level/$', add_level_to_chapter_view, name='add_level_to_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/remove_level/$', remove_level_from_chapter_view, name='remove_level_from_chapter'),
    url(r'^level/(\d+)/template/(\d+)/add_template/$', add_template_to_level_view, name='add_template_to_level'),
    url(r'^level/(\d+)/template/(\d+)/remove_template/$', remove_template_from_level_view, name='remove_template_from_level'),
    url(r'^set/(\d+)/stats/$', set_stats_view, name='set_stats'),

    url(r'^set/update/$', update_set_view, name='update_set_view'),
    url(r'^chapter/update/$', update_chapter_view, name='update_chapter_view'),
    url(r'^level/update/$', update_level_view, name='update_level_view'),

    url(r'^add-user-to-set/', add_user_to_set_view, name='add_user_to_set'),
    # DJANGO SELECTABLE
    # Might be useful for autocomplete for tagging
    # Meant to work with jquery ui https://github.com/mlavin/django-selectable
    url(r'^selectable/', include('selectable.urls')),

    url(r'^format/', format_domain, name='format_db'),
)
