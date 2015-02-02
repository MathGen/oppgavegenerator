from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=200)

class Template(models.Model):
    question_text = models.CharField(max_length=200)
    solution =  models.CharField(max_length=10000)
    answer = models.CharField(max_length=200)
    creator = models.ForeignKey(User)
    creation_date = models.DateTimeField('date created')
    variables = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField()
    times_solved = models.PositiveIntegerField()
    times_failed = models.PositiveIntegerField()
    topic = models.ForeignKey(Topic)

