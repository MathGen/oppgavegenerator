# predefined tables to be rendered with django-tables
__author__ = 'eirikk'

import django_tables2 as tables
from oppgavegen.models import Template

class TemplateTable(tables.Table):
    View = tables.TemplateColumn('<a href="/?q={{record.id}}">View</a>')

    class Meta:
        model = Template
        attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id","question_text", "creator", "topic", "type", "rating")

