"""

Contains various forms that are used in views

"""
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django import forms
from haystack.forms import SearchForm
from registration.users import UserModel
from registration.forms import RegistrationFormUniqueEmail

from oppgavegen.models import Set, Chapter, Level, Template, Tag

User = UserModel()

class NamedUserRegistrationForm(RegistrationFormUniqueEmail):
    """ Registration form that requires the users full name and a unique e-mail address """
    required_css_class = 'required'
    username = forms.CharField(label="Brukernavn", required=True, max_length=30)
    email = forms.EmailField(label="E-postadresse", required=True)
    first_name = forms.CharField(label="Fornavn", required=True)
    last_name = forms.CharField(label="Etternavn", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class NamedUserDetailsForm(ModelForm):
    """ Form for updating user's own details """
    first_name = forms.CharField(label="Fornavn", required=False)
    last_name = forms.CharField(label="Etternavn", required=False)
    email = forms.EmailField(label="E-postadresse", required=False)

    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class TagField(forms.CharField):
    """
    Return a list of Tag-objects.
    Creates new Tag-objects if they don't already exist in the database.
    """
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
    q = forms.CharField(required=False,label='',
                        widget=forms.TextInput(attrs={'type': 'search', 'placeholder' : 'Søk i oppgavemaler'}))
    name = forms.CharField(required=False, label='Tittel',
                           widget=forms.TextInput(attrs={'type': 'text', 'placeholder' : 'Oppgavetittel'}))
    creator = forms.CharField(required=False, label='Forfatter',
                              widget=forms.TextInput(attrs={'type': 'text', 'placeholder' : 'Forfatter'}))
    min_rating = forms.IntegerField(required=False, label='Lavest Rating',
                                    widget=forms.NumberInput(attrs={'class': 'numberinput', 'type': 'number',
                                                                    'max': '9999', 'placeholder' : 'Minimum'}))
    max_rating = forms.IntegerField(required=False, label='Høyest Rating',
                                    widget=forms.NumberInput(attrs={'class': 'numberinput', 'type': 'number',
                                                                    'max': '9999', 'placeholder' : 'Maximum'}))
    multiple_support = forms.BooleanField(required=False, label='Flervalg')
    fill_in_support = forms.BooleanField(required=False, label='Utfylling')
    # multifill_support = forms.BooleanField(required=False, label='Flervalg med utfylling')

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(TemplateSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check for name input
        if self.cleaned_data['name']:
            sqs = sqs.filter(name__contains=self.cleaned_data['name'])

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
        if self.cleaned_data['multiple_support']:
            sqs = sqs.filter(multiple_support='True')

        # Check for fill-in filter
        if self.cleaned_data['fill_in_support']:
            sqs = sqs.filter(fill_in_support='True')

        # Check for multifill filter
        # if self.cleaned_data['multifill_support']:
        #    sqs = sqs.filter(multifill_support='True')

        return sqs


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


class QuestionForm(forms.Form):
    """ Math problem answer submission form """
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
