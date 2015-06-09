from django.contrib import admin
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import ExtendedUser
from oppgavegen.models import Level
from oppgavegen.models import Chapter
from oppgavegen.models import Set
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin



class topicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')


class templateAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date', 'question_text', 'answer','creator', 'times_solved', 'times_failed')

class ExtendedInline(admin.StackedInline):
    model = ExtendedUser
    can_delete = False
    verbose_name_plural = 'extendeduser'


class UserAdmin(UserAdmin):
    inlines = (ExtendedInline, )

class levelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class chapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class setAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Template, templateAdmin)
admin.site.register(Topic,  topicAdmin)
admin.site.register(Level,  levelAdmin)
admin.site.register(Chapter,  chapterAdmin)
admin.site.register(Set,  setAdmin)