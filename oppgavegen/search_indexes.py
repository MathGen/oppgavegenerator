"""

Search Indexes for use in Haystack

"""

import datetime
from haystack import indexes
from oppgavegen.models import Template, Set, Chapter, Level

class TemplateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    question_text = indexes.CharField(model_attr='question_text_latex')
    solution_text = indexes.CharField(model_attr='solution_latex')
    creator = indexes.CharField(model_attr='creator')
    creation_date = indexes.DateTimeField(model_attr='creation_date', indexed=False)
    rating = indexes.IntegerField(model_attr='rating', indexed=False)
    multiple = indexes.BooleanField(model_attr='multiple_support', default='false', indexed=False)
    fill_in = indexes.BooleanField(model_attr='fill_in_support', default='false', indexed=False)
    levels = indexes.MultiValueField()
    tags = indexes.MultiValueField()

    def prepare_levels(self, object):
        return [level.name for level in object.levels.all()]

    def prepare_tags(self, object):
        return [tag.name for tag in object.tags.all()]

    def get_model(self):
        return Template

    def index_queryset(self, using=None):
        """Used when the entire index for the model is updated."""
        return self.get_model().objects.filter(creation_date__lte=datetime.datetime.now())

class SetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    creator = indexes.CharField(model_attr='creator')
    # chapters=indexes.MultiValueField()

    # def prepare_chapters(self, object):
    #     return [chapter.name for chapter in object.chapters.all()]

    def get_model(self):
        return Set

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ChapterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    creator = indexes.CharField(model_attr='creator')
    # levels = indexes.MultiValueField()

    # def prepare_levels(self, object):
    #   return [level.name for level in object.levels.all()]

    def get_model(self):
        return Chapter

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class LevelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    creator = indexes.CharField(model_attr='creator')

    def get_model(self):
        return Level

    def index_queryset(self, using=None):
        return self.get_model().objects.all()