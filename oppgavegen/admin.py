from django.contrib import admin
from oppgavegen.models import Template
from oppgavegen.models import Topic
from oppgavegen.models import TemplateType

class topicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')

class templateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')

class templateAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date', 'question_text', 'answer','creator', 'times_solved', 'times_failed')

admin.site.register(Template, templateAdmin)
admin.site.register(Topic,  topicAdmin)
admin.site.register(TemplateType, templateTypeAdmin)
