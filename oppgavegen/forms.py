from django.forms import ModelForm
from django.forms import forms
from django import forms
from haystack.forms import SearchForm
from .models import Set
from .models import Level
from .models import Template

class TemplateSearchForm(SearchForm):
    title = forms.CharField(required=False)
    tags = forms.CharField(required=False)
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

        # Check for title input
        if self.cleaned_data['title']:
            sqs = sqs.filter(title__contains=self.cleaned_data['title'])

        # Check for creator input
        if self.cleaned_data['creator']:
            sqs = sqs.filter(creator__username__contains=self.cleaned_data['creator'])

        # Check for tags input
        if self.cleaned_data['tags']:
            sqs = sqs.filter(tag__name__contains=self.cleaned_data['tags'])

        # Check for max rating input
        if self.cleaned_data['max_rating']:
            sqs = sqs.filter(rating__lt=self.cleaned_data['max_rating'])

        # Check for min rating input
        if self.cleaned_data['min_rating']:
            sqs = sqs.filter(rating_gt=self.cleaned_data['min_rating'])

        # Check for min rating input
        if self.cleaned_data['multiple']:
            sqs = sqs.filter(rating_gt=self.cleaned_data['min_rating'])

        # Check for min rating input
        if self.cleaned_data['min_rating']:
            sqs = sqs.filter(rating_gt=self.cleaned_data['min_rating'])

        return sqs


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ('name', 'chapter')


class LevelForm(ModelForm):
    class Meta:
        model = Level
        fields = ('name', 'template')