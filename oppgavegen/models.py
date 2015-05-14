from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# This file contains the models for the database that are not default models in Django (i.e. Users)
# It also contains extensions to the default models in Django.
# The classes have to be in order.
# The reason is that you might try to make a foreign key on a class that does not exist yet.


class Topic(models.Model):
    topic = models.CharField(max_length=200)  # Name of the topic.

    def __str__(self):  # Makes it so that self.topic shows up instead of topic(object)
        """Returns the objects topic"""
        return self.topic

    def clean(self):  # Removes trailing whitespace from topic
        """Returns the topic without whitespace"""
        if self.topic:
            self.topic = self.topic.strip()

# Choices for valid_flag.
valid_choices = (
    (True, 'Valid'),
    (False, 'Invalid')
)


class Template(models.Model):
    """Stores information for Templates"""
    question_text = models.CharField(max_length=200)  # Math expression or text question ex. "Solve: ax = b + cx"
    solution = models.CharField(max_length=10000)  # Step by step solution to the answer
    answer = models.CharField(max_length=200)  # The answer of the question.
    creator = models.ForeignKey(User, blank=True, null=True)  # User ID of creator of template
    creation_date = models.DateTimeField('date created', blank=True, null=True)  # Date and time of creation
    rating = models.PositiveSmallIntegerField(blank=True, null=True)  # Difficulty rating. Defaults to 1200.
    times_solved = models.PositiveIntegerField(blank=True, null=True)  # Times the problem has been solved.
    times_failed = models.PositiveIntegerField(blank=True, null=True)  # Times the problem has not been solved.
    topic = models.ForeignKey(Topic)  # ID of the topic this problem belongs to ex. 2 (where 2 means algebra.)
    random_domain = models.CharField(max_length=250, blank=True, null=True)
    # random_domain: Space separated string with 3 numbers denoting which values the random numbers can be-
    # and how manny decimals the number has. ie. 1 10 0 -> integers from 1 to 10.
    choices = models.CharField(max_length=700, blank=True, null=True)  # Holds the choices for multiple choice.
    dictionary = models.CharField(max_length=10000, blank=True, null=True, default="")
    conditions = models.CharField(max_length=10000, blank=True, null=True, default="")
    fill_in = models.CharField(max_length=10000, blank=True, null=True, default="")
    valid_flag = models.BooleanField(default=False, choices=valid_choices)
    disallowed = models.CharField(max_length=1000, blank=True, null=True, default="")
    multiple_support = models.BooleanField(default=False)  # Denotes whether the template supports multiple choice
    fill_in_support = models.BooleanField(default=False)  # Denotes whether the template supports fill in the blanks

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
        return self.question_text


class ExtendedUser(models.Model):
    """Extends the default django user model with a one to one relation"""
    user = models.OneToOneField(User)
    rating = models.rating = models.PositiveSmallIntegerField(default=1200)
    current_template = models.rating = models.SmallIntegerField(default=-1)


def create_user_profile(sender, instance, created, **kwargs):
    """Adds a ExtendedUser to a new user when created with one to one relation"""
    if created:
       profile, created = ExtendedUser.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
