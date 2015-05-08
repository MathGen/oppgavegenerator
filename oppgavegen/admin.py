from django.contrib import admin
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import TemplateType
from oppgavegen.models import ExtendedUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class topicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')

class templateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')

class templateAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date', 'question_text', 'answer','creator', 'times_solved', 'times_failed')

class ExtendedInline(admin.StackedInline):
    model = ExtendedUser
    can_delete = False
    verbose_name_plural = 'extendeduser'


class UserAdmin(UserAdmin):
    inlines = (ExtendedInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Template, templateAdmin)
admin.site.register(Topic,  topicAdmin)
admin.site.register(TemplateType, templateTypeAdmin)
