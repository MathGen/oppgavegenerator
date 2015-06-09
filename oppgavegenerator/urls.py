from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    url(r'^task/$', 'oppgavegen.views.task'),
    url(r"^task/([\w ]+)/$", 'oppgavegen.views.task_by_extra', name='task_by_extra'),
    url(r"^task/(\d+)/([\w ]+)/$", 'oppgavegen.views.task_by_id_and_type', name='task_by_id_and_type'),
    url(r"^edit/(\d+)/$", 'oppgavegen.views.edit_template', name='edit_template'),
    url(r'^useranalysis/', 'oppgavegen.views.user_overview_table', name='user_table'),
    url(r'^search/', include( 'ajaxsearch.urls' )),
)
