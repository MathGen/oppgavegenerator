from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=200)                # Name of the topic.

class Template(models.Model):
    question_text = models.CharField(max_length=200)       # The template. Math expression or text question ex. "Solve: ax = b + cx"
    solution =  models.CharField(max_length=10000)           # Step by step solution to the answer
    answer = models.CharField(max_length=200)                # A simple math operation to calculate the problem template. Should be the last step in the solution.
    creator = models.ForeignKey(User)                             # User ID of creator of template
    creation_date = models.DateTimeField('date created')    # Date and time of creation
    variables = models.PositiveSmallIntegerField()            # A number of how many variables are in the problem template.
    rating = models.PositiveSmallIntegerField()                # Difficulty rating. Defaults to 1200.
    times_solved = models.PositiveIntegerField()              # Amount of times the problem has been solved.
    times_failed = models.PositiveIntegerField()              # Amount of times the problem has not been solved (wrong answer.)
    topic = models.ForeignKey(Topic)                              # ID of the topic this problem belongs to ex. 2 (where 2 means algebra.)
    number_of_decimals = models.PositiveSmallIntegerField()
    answer_can_be_zero = models.BooleanField()

