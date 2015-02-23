from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'oppgavegen.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/', 'oppgavegen.views.index', name='index'),
    url(r'^answers/', 'oppgavegen.views.answers', name='answers'),
    url(r'^playground/', 'oppgavegen.views.playground', name='playground'),
    url(r'^test/', 'oppgavegen.views.test', name='test'),
    url(r'^gen/', 'oppgavegen.views.gen', name='gen'),
    url(r'^submit/', 'oppgavegen.views.submit', name='submit'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('registration.backends.simple.urls')),              # registration views
)
