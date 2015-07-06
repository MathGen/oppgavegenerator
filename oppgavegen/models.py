"""
 Defines the models for the database that are not default models in Django (i.e. Users)
 It also contains extensions to the default models in Django.
 The classes have to be in order as foreign keys must be from existing classes.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# This file contains the models for the database that are not default models in Django (i.e. Users)
# It also contains extensions to the default models in Django.
# The classes have to be in order.
# The reason is that you might try to make a foreign key on a class that does not exist yet.

class Tag(models.Model):
    """Searchable tags for problem templates."""
    name = models.CharField(max_length=200, unique=True)  # Name of the tag.

    def __str__(self):  # Makes it so that self.topic shows up instead of topic(object)
        """Returns the objects topic"""
        return self.name

# Choices for valid_flag.
valid_choices = (
    (True, 'Valid'),
    (False, 'Invalid')
)


class Template(models.Model):
    """Stores information for Templates"""
    name = models.CharField(max_length=50, blank=True, default='Uten Tittel') # The template name. Main identifier for teacher users.
    tags = models.ManyToManyField(Tag, blank=True)  # Template tags. Tags should describe content of math problems i.e "arithmetic"
    question_text = models.CharField(max_length=2000)  # Math expression or text question ex. "Solve: ax = b + cx"
    solution = models.CharField(max_length=10000)  # Step by step solution to the answer
    answer = models.CharField(max_length=200)  # The answer of the question.
    creator = models.ForeignKey(User, blank=True, null=True, related_name='templates_created')  # User ID of creator of template
    editor = models.ForeignKey(User, blank=True, null=True, related_name='templates_edited')  # Editor of template

    creation_date = models.DateTimeField('date created', blank=True, null=True)  # Date and time of creation
    rating = models.PositiveSmallIntegerField(blank=True, null=True, default=1200)  # Difficulty rating.
    fill_rating = models.PositiveSmallIntegerField(blank=True, null=True, default=1150)  # Rating for fill.
    choice_rating = models.PositiveSmallIntegerField(blank=True, null=True, default=1100)  # Rating for multiple choice.
    times_solved = models.PositiveIntegerField(blank=True, null=True)  # Times the problem has been solved.
    times_failed = models.PositiveIntegerField(blank=True, null=True)  # Times the problem has not been solved.
    random_domain = models.CharField(max_length=250, blank=True, null=True)
    # random_domain: Space separated string with 3 numbers denoting which values the random numbers can be-
    # and how manny decimals the number has. ie. 1 10 0 -> integers from 1 to 10.
    difficulty = models.PositiveSmallIntegerField(default=14, blank=True)
    difficulty_multiple = models.PositiveSmallIntegerField(default=14, blank=True)
    difficulty_blanks = models.PositiveSmallIntegerField(default=14, blank=True)

    choices = models.CharField(max_length=700, blank=True, null=True)  # Holds the choices for multiple choice.
    dictionary = models.CharField(max_length=10000, blank=True, null=True, default="")
    conditions = models.CharField(max_length=10000, blank=True, null=True, default="")
    fill_in = models.CharField(max_length=10000, blank=True, null=True, default="")
    valid_flag = models.BooleanField(default=False, choices=valid_choices)
    disallowed = models.CharField(max_length=5000, blank=True, null=True, default="")
    required = models.CharField(max_length=5000, blank=True, null=True, default="")
    multiple_support = models.BooleanField(default=False)  # Denotes whether the template supports multiple choice
    fill_in_support = models.BooleanField(default=False)  # Denotes whether the template supports fill in the blanks
    margin_of_error = models.PositiveIntegerField(default=0, null=True, blank=True)

    # Also save the original latex for post-back:
    used_variables = models.CharField(max_length=200, blank=True, null=True)
    question_text_latex = models.CharField(max_length=200, blank=True, null=True)
    solution_latex = models.CharField(max_length=10000, blank=True, null=True)
    answer_latex = models.CharField(max_length=200, blank=True, null=True)
    choices_latex = models.CharField(max_length=700, blank=True, null=True)
    conditions_latex = models.CharField(max_length=10000, blank=True, null=True, default="")
    fill_in_latex = models.CharField(max_length=10000, blank=True, null=True, default="")
    calculation_ref = models.CharField(max_length=1000, blank=True, null=True)
    unchanged_ref = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):  # Makes it so that self.question_text shows up instead of topic(object)
        """Returns the question_text field of the object"""
        return str(self.pk) + ':   ' + self.question_text


class Level(models.Model):
    """Stores sets of templates"""
    name = models.CharField(max_length=200)  # Name of the topic.
    templates = models.ManyToManyField(Template, related_name='levels',blank=True) # List of templates in level
    creator = models.ForeignKey(User, blank=True, null=True, related_name='levels_created')
    editor = models.ForeignKey(User, blank=True, null=True, related_name='levels_edited')  # Editor of template
    creation_date = models.DateTimeField('date created', blank=True, null=True, auto_now_add=True)  # Date and time of creation
    k_factor = models.PositiveIntegerField(default=3, null=True, blank=True)  # Decides how fast a user progress
    offset = models.IntegerField(default=0, null=True, blank=True)  # Offset for the level.

    def __str__(self):  # return self.name instead of level-object
        """Returns the level name"""
        return str(self.pk) + ':   ' + self.name


class Chapter(models.Model):
    """Stores sets of levels"""
    name = models.CharField(max_length=200)  # Name of the topic.
    levels = models.ManyToManyField(Level, related_name='chapters', blank=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name='chapters_created')
    editor = models.ForeignKey(User, blank=True, null=True, related_name='chapters_edited')  # Editor of template
    creation_date = models.DateTimeField('date created', blank=True, null=True, auto_now_add=True)  # Date and time of creation
    order = models.CharField(max_length=400, default='', blank=True) #CSV list of the order of levels.

    def __str__(self):  # Makes it so that self.name shows up instead of set(object)
        """Returns the chapter name"""
        return str(self.pk) + ':   ' + self.name


class Set(models.Model):
    """Stores sets of chapters"""
    name = models.CharField(max_length=200)  # Name of the topic.
    chapters = models.ManyToManyField(Chapter, related_name='sets', blank=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name='sets_created')
    editor = models.ForeignKey(User, blank=True, null=True, related_name='sets_edited')  # Editor of template
    creation_date = models.DateTimeField('date created', blank=True, null=True, auto_now_add=True)  # Date and time of creation
    order = models.CharField(max_length=400, default='')

    def __str__(self):  # Makes it so that self.name shows up instead of set(object)
        """Returns the set name"""
        return self.name


class UserLevelProgress(models.Model):
    """Stores the users progress on a level"""
    user = models.ForeignKey(User, blank=True, null=True)
    level = models.ForeignKey(Level, blank=True, null=True, related_name='student_progresses')
    level_rating = models.IntegerField(default=1200)
    stars = models.IntegerField(default=0)
    questions_answered = models.PositiveIntegerField(default=0)

    def __str__(self):  #  Returns the pk
        return str(self.pk)


class ExtendedUser(models.Model):
    """Extends the default django user model with a one to one relation"""
    user = models.OneToOneField(User)
    rating = models.PositiveSmallIntegerField(default=1200) #may not be needed in the new system
    current_template = models.SmallIntegerField(default=-1) # Might be redundant in the new system
    # It would have to keep track of which level the user is on and what task is given there
    # Making a abandonment system is probably better. where the user is forced to finish the template or lose
    # rating/stars.
    winstreak = models.SmallIntegerField(default=0)
    current_level = models.OneToOneField(Level, null=True, blank=True)
    current_chapter = models.OneToOneField(Chapter, null=True, blank=True)
    current_set = models.OneToOneField(Set, null=True, blank=True)

    def current_level_template_ids(self):
        """ Return list of template id's in users current level for simple comparisons with search results """
        ids = []
        templates = self.current_level.templates.all()
        for e in templates:
            ids.append(e.id)
        return ids

    def current_chapter_level_ids(self):
        """ Return list of level id's in users current chapter for simple comparisons with search results """
        ids = []
        levels = self.current_chapter.levels.all()
        for e in levels:
            ids.append(e.id)
        return ids

    def current_set_chapter_ids(self):
        """ Return list of chapter id's in users current set for simple comparisons with search results """
        ids = []
        chapters = self.current_chapter.levels.all()
        for e in chapters:
            ids.append(e.id)
        return ids


def create_user_profile(sender, instance, created, **kwargs):
    """Adds a ExtendedUser to a new user when created with one to one relation"""
    if created:
       profile, created = ExtendedUser.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
