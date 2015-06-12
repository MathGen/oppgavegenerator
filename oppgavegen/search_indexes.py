"""

Search Indexes for use in Haystack

"""

import datetime
from haystack import indexes
from .models import Template
from .models import Tag

class TemplateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    question_text = indexes.CharField(model_attr='question_text_latex')
    solution_text = indexes.CharField(model_attr='solution_latex')
    creator = indexes.CharField(model_attr='creator')
    creation_date = indexes.DateTimeField(model_attr='creation_date', indexed=False)
    rating = indexes.IntegerField(model_attr='rating', indexed=False)
    multiple = indexes.BooleanField(model_attr='multiple_support', default='false', indexed=False)
    fill_in = indexes.BooleanField(model_attr='fill_in_support', default='false', indexed=False)
    tags = indexes.MultiValueField()

    def prepare_tags(self, object):
        return [tag.name for tag in object.tags.all()]

    def get_model(self):
        return Template

    def index_queryset(self, using=None):
        """Used when the entire index for the model is updated."""
        return self.get_model().objects.filter(creation_date__lte=datetime.datetime.now())