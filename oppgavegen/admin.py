from django.contrib import admin
from oppgavegen.models import Template
from oppgavegen.models import Topic

class topicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')

class templateAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date', 'question_text', 'answer','creator', 'times_solved', 'times_failed')

admin.site.register(Template, templateAdmin)
admin.site.register(Topic,  topicAdmin)
