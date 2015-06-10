# Haystack Search Indexes

import datetime
from haystack import indexes
from .models import Template

class TemplateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='creator')
    creation_date = indexes.DateTimeField(model_attr='creation_date')
    rating = indexes.IntegerField(model_attr='rating')
    multiple = indexes.BooleanField(model_attr='multiple_support')
    fill_in = indexes.BooleanField(model_attr='fill_in_support')

    def get_model(self):
        return Template

    def index_queryset(self, using=None):
        """Used when the entire index for the model is updated."""
        return self.get_model().objects.filter(creation_date__lte=datetime.datetime.now())