"""Defines tables and their data sources to be rendered in HTML with django-tables2 """

import django_tables2 as tables
from oppgavegen.models import Template
from oppgavegen.models import ExtendedUser
from oppgavegen.models import Topic

class TemplateTable(tables.Table):
    """ Generate a html table with all templates marked valid. """

    dropdownhtml = '<div class="btn-group">' \
                   '<a href="#" class="dropdown-toggle" data-toggle="dropdown">View<b class="caret"></b></a>' \
                   '<ul class="dropdown-menu dropdown-menu-right" role="menu">' \
                   '<li><a href="{% url "task_by_extra" record.id %}">Normal</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "blanks" %}">Fill in the Blanks</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "multiple" %}">Multiple Choice</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "multifill" %}">Multiple Fill-Ins</a></li>' \
                   '</ul>' \
                   '</div>'

    view = tables.TemplateColumn(dropdownhtml, orderable=False)
    content = tables.TemplateColumn('<div class="input_field" style="width:400px;padding:-5px;margin:-5px;">'
                                    '<span class="mathquill-embedded-latex input_mathquill" style="font-size:1.2em;width:parent;">'
                                    '{{record.question_text_latex}}'
                                    '</span></div>')
    multiple_support = tables.BooleanColumn(verbose_name='MC')
    fill_in_support = tables.BooleanColumn(verbose_name='FI')

    class Meta:
        model = Template
        template = ("bstable.html")
        # attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id", "creator", "topic", "multiple_support", "fill_in_support", "rating")
        sequence = ("id", "content", "creator", "topic", "multiple_support", "fill_in_support", "rating", "view")
        order_by = "-id"


class UserTemplatesTable(tables.Table):
    """Generate a html table with the logged in users own templates, and an action menu."""
    dropdownhtml = '<div class="btn-group">' \
                   '<button type="button" class="btn btn-primary btn-xs dropdown-toggle" data-toggle="dropdown">' \
                   '<span class="caret"></span>' \
                   '<span class="sr-only">Toggle Dropdown</span>' \
                   '</button>' \
                   '<ul class="dropdown-menu dropdown-menu-right" role="menu">' \
                   '<li><a href="{% url "task_by_extra" record.id %}">Normal</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "blanks" %}">Fill in the Blanks</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "multiple" %}">Multiple Choice</a></li>' \
                   '<li><a href="{% url "task_by_id_and_type" record.id "multifill" %}">Multiple Fill-Ins</a></li>' \
                   '<li role="presentation" class="divider"></li>' \
                   '<li><a href="{% url "edit_template" record.id %}">Edit</a></li>' \
                   '</ul>' \
                   '</div>'

    action = tables.TemplateColumn(dropdownhtml, orderable=False)
    content = tables.TemplateColumn('<div class="input_field" style="width:400px;padding:-5px;margin:-5px;">'
                                    '<span class="mathquill-embedded-latex input_mathquill" style="font-size:1.2em;width:parent;">'
                                    '{{record.question_text_latex}}'
                                    '</span></div>')
    multiple_support = tables.BooleanColumn(verbose_name='MC')
    fill_in_support = tables.BooleanColumn(verbose_name='FI')

    class Meta:
        model = Template
        template = ("bstable.html")
        # attrs = {"class": "paleblue"} # add class="paleblue" (table theme) to <table> tag
        # fields to include in table (displayed in this order)
        fields = ("id", "topic", "multiple_support", "fill_in_support", "rating")
        sequence = ("id", "content", "topic", "multiple_support", "fill_in_support", "rating", "action")
        order_by = ("-id")

class UserTable(tables.Table):
    """Generate a table of all users and their current rating."""

    class Meta:
        model = ExtendedUser
        template = ("bstable.html")
        fields = ("id", "user", "rating")

