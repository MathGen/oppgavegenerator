"""

Configures how urls for the site works

WARNING:
If a url is marked with a "# JS:" comment you need to be careful
about changing the url without changing the (dynamically)
formed urls in the javascript file listed.

Most other ones can most likely be changed and Django's
reverse url lookup by name will make sure the correct url is formed.


"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from haystack.query import SearchQuerySet

from haystack.views import search_view_factory

from oppgavegen.views.views import *
from oppgavegen.views.stat_views import *
from oppgavegen.forms import *
from oppgavegen.views.add_remove_views import *
from oppgavegen.views.game_views import *
from oppgavegen.views.level_editor_views import *
from oppgavegen.view_logic.db_format import format_domain

from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', index, name='index'),

    # Template creation, editing and submission
    url(r'^newtemplate/', new_template, name='newtemplate'),
    url(r'^edit/(\d+)/$', edit_template, name='edit_template'),
    url(r'^submit/', submit, name='submit'), # JS: gen.js

    # Template overview and copy/delete
    url(r'^templates/$', TemplatesListView.as_view(), name='all_templates_list'),
    url(r'^user/templates/$', UserTemplatesListView.as_view(), name='user_templates_list'),
    url(r'^user/templates/nocopies/$', UserTemplatesListViewNoCopies.as_view(), name='user_original_templates_list'),
    url(r'^template/(\d+)/copy/next/([\w ]+)/$', confirm_template_copy, name='confirm_template_copy'),
    url(r'^template/(\d+)/delete/$', delete_template, name='delete_template'),

    # Problem generation
    url(r'^task/$', task, name='task_by_user_rating'),
    url(r"^task/([\w ]+)/$", task_by_extra, name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", task_by_id_and_type, name='task_by_id_and_type'),
    url(r'^answers/', answers, name='answers'), # JS: gen.js

    # Registration and account management urls
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/register/$', RegistrationView.as_view(form_class=NamedUserRegistrationForm), name='registration_register'),
    url(r'^user/settings/$', UserSettingsView.as_view(), name='user_settings'),
    url(r'^user/settings/deactivate/$', user_deactivate, name='user_deactivate'),

    # Game urls
    url(r'^game/(\d+)/$', game, name='game'),
    url(r'^game/(\d+)/levels/$', levels, name='levels'), # JS: game.js
    url(r'^game/(\d+)/chapters/$', chapters, name='chapters'), # JS: game.js
    url(r'^game/template/$', get_template, name='get_template'), # JS: game.js
    url(r'^game/(\d+)/answer/$', get_solution, name='get_answer'), # JS: game.js
    url(r'^add-user-to-set/', add_user_to_set_view, name='add_user_to_set'), # JS: set_membership_functions.js
    url(r'^remove-user-from-set/', remove_user_from_set_view, name='remove_user_from_set'), #JS: set_membership_funcs.js


    # JS: set_edit_functions.js, search_functions.js
    url(r'^template/([\w ]+)/preview/$', preview_template, name='preview_template'),

    # Sets, chapters and level management urls
    url(r'^user/sets/$', UserSetListView.as_view(), name='user_sets'),
    url(r'^set/(\d+)/chapters/$', SetChapterListView.as_view(), name='chapters_by_set'),
    url(r'^set/(\d+)/useradmin/$', set_students_admin, name='students_by_set'),
    url(r'^set/(\d+)/setpublic/$', set_public, name='set_to_public'),
    url(r'^set/(\d+)/setprivate/$', set_private, name='set_to_private'),
    url(r'^set/(\d+)/stats/$', set_stats_view, name='set_stats'),
    url(r'^chapter/(\d+)/levels/$', ChapterLevelsListView.as_view(), name='levels_by_chapter'),
    url(r'^chapter/(\d+)/stats/$', detailed_chapter_stats, name='chapter_stats'),
    url(r'^level/(\d+)/templates/$', LevelsTemplatesListView.as_view(), name='templates_by_level'),
    url(r'^level/(\d+)/stats/', level_stats, name='level_stats'),

    # All of these are called from set_edit_functions.js
    url(r'^set/([\w ]+)/new_set/$', new_set_view, name='new_set_view'),
    url(r'^set/([\w ]+)/add/$', add_set_to_user_view, name='add_set_view'),
    url(r'^set/([\w ]+)/newreq/$', copy_set_as_requirement, name='copy_set_as_requirement'),
    url(r'^set/(\d+)/remove/$', remove_set_view, name='remove_set_view'),
    url(r'^set/(\d+)/([\w ]+)/new_chapter/$', new_chapter_for_set, name='new_chapter_for_set'),
    url(r'^set/(\d+)/chapter/(\d+)/add/$', add_chapter_to_set_view, name='add_chapter_to_set'),
    url(r'^set/(\d+)/chapter/(\d+)/remove/$', remove_chapter_from_set_view, name='remove_chapter_from_set'),

    url(r'^chapter/(\d+)/([\w ]+)/new_level/$', new_level_for_chapter, name='new_level_for_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/add/$', add_level_to_chapter_view, name='add_level_to_chapter'),
    url(r'^chapter/(\d+)/level/(\d+)/remove/$', remove_level_from_chapter_view, name='remove_level_from_chapter'),

    url(r'^level/(\d+)/template/(\d+)/add/$', add_template_to_level_view, name='add_template_to_level'),
    url(r'^level/(\d+)/template/(\d+)/remove/$', remove_template_from_level_view, name='remove_template_from_level'),

    url(r'^set/update/$', update_set_view, name='update_set_view'),
    url(r'^chapter/update/$', update_chapter_view, name='update_chapter_view'),
    url(r'^level/update/$', update_level_view, name='update_level_view'),

    # Haystack search urls

    # Search templates
    url(r'^templates/search/$', search_view_factory(
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template', copy=False).order_by('creation_date'),
        template='search/template_search.html',
        form_class=TemplateSearchForm,
    ), name='templates_search'),

    # Compact search views (for ajax loading)
    url(r'^minisearch/sets/$', search_view_factory( # JS: set_edit_functions.js
        template='search/compact_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.set', copy=False),
        results_per_page=100
    )),
    url(r'^minisearch/chapters/$', search_view_factory( # JS: set_edit_functions.js
        template='search/compact_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.chapter', copy=False),
        results_per_page=100
        )),
    url(r'^minisearch/levels/$', search_view_factory( # JS: set_edit_functions.js
        template='search/compact_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.level', copy=False),
       results_per_page=100
        )),
    url(r'^minisearch/templates/$', search_view_factory( # JS: set_edit_functions.js
        template='search/compact_search.html',
        searchqueryset=SearchQuerySet().filter(django_ct='oppgavegen.template', copy=False).order_by('-creation_date'),
        results_per_page=200
        )),

    #Formats the random_domain for templates from the old format to the new one
    url(r'^format/', format_domain, name='format_db'),
)
