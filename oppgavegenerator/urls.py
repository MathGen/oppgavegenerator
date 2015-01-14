from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oppgavegenerator.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/', 'oppgavegen.views.index', name='index'),
    url(r'^playground/', 'oppgavegen.views.playground', name='playground'),
    url(r'^admin/', include(admin.site.urls)),
)
