"""

Contains various forms that are used in views

"""
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django import forms
from haystack.forms import SearchForm

from .models import Set, Chapter, Level, Template, ExtendedUser, Tag


class TagField(forms.CharField):
    """
    Return a list of Tag-objects.
    Creates new Tag-objects if they don't exist.
    """
    # def prepare_value(self, value):
    def clean(self, value):
        value = super(TagField, self).clean(value)
        values = value.split('§')
        tag_obj = []
        for e in values:
            if Tag.objects.filter(name=e).exists():
                existing_tag = Tag.objects.get(name=e)
                tag_obj.append(existing_tag)
            else:
                newtag = Tag(name=e)
                newtag.save()
                tag_obj.append(newtag)
        try:
            return tag_obj
        except ValueError:
            raise forms.ValidationError("Please provide a paragraph-separated list of tags.")



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

        # Check for name input
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

        return sqs.models(Template)

class SetsSearchForm(SearchForm):
    """ Generic search form for Set, Chapter and Level """

    name = forms.CharField(required=False)
    creator = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(SetsSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check for name input
        if self.cleaned_data['name']:
            sqs = sqs.filter(title__contains=self.cleaned_data['name'])

        # Check for creator input
        if self.cleaned_data['creator']:
            sqs = sqs.filter(creator__username__contains=self.cleaned_data['creator'])

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
    tags_list = TagField(required=False)

    class Meta:
        model = Template
        fields = '__all__'

    def process(self):
        """Returns a cleaned dictionary of it's own values."""
        cd = {'question' : self.cleaned_data['question'],
              'answer' : self.cleaned_data['answer'],
              'tags' : self.cleaned_data['tags_list'],
              'difficulty' : 1 }
        return cd

    def save(self, commit=True):
        self.fields['tags'] = self.cleaned_data['tags_list']
        return super(TemplateForm, self).save(commit=commit)

class UserCurrentSetsForm(ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ('current_set', 'current_chapter', 'current_level',)