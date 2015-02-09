from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#This file contains the models for the database that are not default models in django (i.e. Users)

class Topic(models.Model):
    topic = models.CharField(max_length=200)                  #Name of the topic.
    def __str__(self):                                        #Makes it so that self.topic shows up instead of topic(object)
        return self.topic

    def clean(self):                                          #Removes trailing whitespace from topic
        if self.topic:
            self.topic = self.topic.strip()

class Template(models.Model):
    question_text = models.CharField(max_length=200)          #The template. Math expression or text question ex. "Solve: ax = b + cx"
    solution =  models.CharField(max_length=10000)            #Step by step solution to the answer
    answer = models.CharField(max_length=200)                 #A simple math operation to calculate the problem template. Should be the last step in the solution.
    creator = models.ForeignKey(User)                         #User ID of creator of template
    creation_date = models.DateTimeField('date created')      #Date and time of creation
    variables = models.PositiveSmallIntegerField()            #A number of how many variables are in the problem template.
    rating = models.PositiveSmallIntegerField()               #Difficulty rating. Defaults to 1200.
    times_solved = models.PositiveIntegerField()              #Amount of times the problem has been solved.
    times_failed = models.PositiveIntegerField()              #Amount of times the problem has not been solved (wrong answer.)
    topic = models.ForeignKey(Topic)                          #ID of the topic this problem belongs to ex. 2 (where 2 means algebra.)
    number_of_decimals = models.PositiveSmallIntegerField()   #The number of decimals allowed in the answer.
    answer_can_be_zero = models.BooleanField(default=False)   #True/False for if the answer to a question can be Zero.
    random_domain = models.CharField(max_length=15)           #Space separated string with 2 numbers denoting which values the random numbers can be.
    number_of_answers = models.SmallIntegerField()            #The number of answers to to questions. (i.e. Second-degree polynomial equations may have 2 solutions

    def __str__(self):                                        #Makes it so that self.question_text shows up instead of topic(object)
        return self.question_text

    #todo add random_domain to each individual random variable, yo.