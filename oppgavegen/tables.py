# predefined tables to be rendered with django-tables
__author__ = 'eirikk'

import django_tables2 as tables
from oppgavegen.models import Template

class TemplateTable(tables.Table):
    class Meta:
        model = Template
        attrs = {"class": "paleblue"} #add class="paleblue" (table theme) to <table> tag
