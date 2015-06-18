"""

Contains various forms that are used in views

"""
from .models import Set, Chapter, Level, Template
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import forms
from django import forms
from haystack.forms import SearchForm, ModelSearchForm, FacetedSearchForm
from selectable.forms import AutoCompleteWidget, AutoCompleteSelectMultipleWidget
from .lookups import TemplateLookup


class TemplateSearchForm(SearchForm):
    name = forms.CharField(required=False)
    creator = forms.CharField(required=False)
    min_rating = forms.IntegerField(required=False)
    max_rating = forms.IntegerField(required=False)
    multiple = forms.BooleanField(required=False)
    fill_in = forms.BooleanField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(TemplateSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check for bane input
        if self.cleaned_data['name']:
            sqs = sqs.filter(title__contains=self.cleaned_data['name'])

        # Check for creator input
        if self.cleaned_data['creator']:
            sqs = sqs.filter(creator__username__contains=self.cleaned_data['creator'])

        # Check for min rating input
        if self.cleaned_data['min_rating']:
            sqs = sqs.filter(rating__gte=self.cleaned_data['min_rating'])

        # Check for max rating input
        if self.cleaned_data['max_rating']:
            sqs = sqs.filter(rating__lte=self.cleaned_data['max_rating'])

        # Check for multiple-choice filter
        if self.cleaned_data['multiple']:
            #sqs = sqs.filter(multiple_support=self.cleaned_data['multiple'])
            sqs = sqs.filter(multiple='True')

        # Check for fill-in filter
        if self.cleaned_data['fill_in']:
            #sqs = sqs.filter(fill_in_support=self.cleaned_data['fill_in'])
            sqs = sqs.filter(fill_in='True')

        return sqs


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ('name', 'chapters')


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('name', 'levels')

class ChapterNameForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ('name',)

class BaseChapterNameFormSet(BaseFormSet):
    # Return a formset for all chapter names in spesific set
    def __init__(self, *args, **kwargs):
        super(BaseChapterNameFormSet, self).__init__(*args, **kwargs)
        self.queryset = Set.chapters.all()

# class LevelForm(ModelForm):
#     class Meta:
#         model = Level
#         fields = ('name', 'templates')

class LevelCreateForm(ModelForm):
    templates = forms.ModelMultipleChoiceField(
        queryset=Template.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Level
        fields = ('name', 'templates')


class QuestionForm(forms.Form):
    user_answer = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400)
    primary_key = forms.IntegerField()
    variable_dictionary = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    template_specific = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    template_type = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=50)
    replacing_words = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)
    disallowed = forms.CharField(widget=forms.widgets.HiddenInput(), max_length=400, required=False)

    def process(self):
        """Returns a cleaned dictionary of it's own values."""
        cd = {'variable_dictionary': self.cleaned_data['variable_dictionary'],
              'primary_key': self.cleaned_data['primary_key'],
              'user_answer': self.cleaned_data['user_answer'],
              'template_type': self.cleaned_data['template_type'],
              'template_specific': self.cleaned_data['template_specific'],
              'replacing_words': self.cleaned_data['replacing_words'],
              'disallowed': self.cleaned_data['disallowed']}
        return cd

class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__'

        def process(self):
            """Returns a cleaned dictionary of it's own values."""
            cd = {self.cleaned_data['question'], self.cleaned_data['answer']}
            return cd