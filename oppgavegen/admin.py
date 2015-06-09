from django.contrib import admin
from oppgavegen.models import Template, Topic, ExtendedUser, Level, Chapter, Set, Tag
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


class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Template, templateAdmin)
admin.site.register(Topic,  topicAdmin)
admin.site.register(Level,  LevelAdmin)
admin.site.register(Chapter,  ChapterAdmin)
admin.site.register(Set,  SetAdmin)
admin.site.register(Tag,  TagAdmin)