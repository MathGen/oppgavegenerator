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
    editor = indexes.CharField(model_attr='editor')
    creation_date = indexes.DateTimeField(model_attr='creation_date', indexed=False)
    rating = indexes.IntegerField(model_attr='rating', indexed=False)
    choice_rating = indexes.IntegerField(model_attr='choice_rating', indexed=False)
    fill_rating = indexes.IntegerField(model_attr='fill_rating', indexed=False)
    #multifill_rating = indexes.IntegerField(model_attr='multifill_rating', indexed=False)
    multiple_support = indexes.CharField(model_attr='multiple_support', indexed=False)
    fill_in_support = indexes.CharField(model_attr='fill_in_support', indexed=False)
    multifill_support = indexes.CharField(model_attr='multifill_support', indexed=False)
    copy = indexes.BooleanField(model_attr='copy', default='false', indexed=False)
    levels = indexes.MultiValueField()
    tags = indexes.MultiValueField()

    def prepare_multiple_support(self, object):
        """ Store boolean value as string """
        str = 'False'
        if object.multiple_support == True:
            str = 'True'
        return str

    def prepare_fill_in_support(self, object):
        """ Store boolean value as string """
        str = 'False'
        if object.fill_in_support == True:
            str = 'True'
        return str

    def prepare_multifill_support(self, object):
        """ Store boolean value as string """
        str = 'False'
        if object.multifill_support == True:
            str = 'True'
        return str

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
    copy = indexes.BooleanField(model_attr='copy', default='false', indexed=False)
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
    copy = indexes.BooleanField(model_attr='copy', default='false', indexed=False)
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
    copy = indexes.BooleanField(model_attr='copy', default='false', indexed=False)

    def get_model(self):
        return Level

    def index_queryset(self, using=None):
        return self.get_model().objects.all()