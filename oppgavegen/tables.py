# predefined tables to be rendered with django-tables

import django_tables2 as tables
from oppgavegen.models import Template

class TemplateTable(tables.Table):
    View = tables.TemplateColumn('<a href="../task/{{record.id}}">View</a>', orderable=False)

    class Meta:
        model = Template
        attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id","question_text", "creator", "topic", "type", "rating")

class BootstrapTemplateTable(tables.Table):
    Normal = tables.TemplateColumn('<a href="../task/{{record.id}}/">View</a>', orderable=False)
    Blanks = tables.TemplateColumn('<a href="../task/{{record.id}}/blanks">View</a>', orderable=False)
    Multiple = tables.TemplateColumn('<a href="../task/{{record.id}}/multiple">View</a>', orderable=False)
    Multifill = tables.TemplateColumn('<a href="../task/{{record.id}}/multifill">View</a>', orderable=False)

    class Meta:
        model = Template
        template = ("bstable.html")
        #attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id","question_text", "creator", "topic", "type", "rating")

class UserTemplates(tables.Table):
    Normal = tables.TemplateColumn('<a href="../task/{{record.id}}/">View</a>', orderable=False)
    Blanks = tables.TemplateColumn('<a href="../task/{{record.id}}/blanks">View</a>', orderable=False)
    Multiple = tables.TemplateColumn('<a href="../task/{{record.id}}/multiple">View</a>', orderable=False)
    Multifill = tables.TemplateColumn('<a href="../task/{{record.id}}/multifill">View</a>', orderable=False)
    Edit = tables.TemplateColumn("<a href={% url 'edit_template' record.id %}>Edit</a>", orderable=False)

    class Meta:
        model = Template
        template = ("bstable.html")
        #attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id","question_text", "topic", "type", "rating")

