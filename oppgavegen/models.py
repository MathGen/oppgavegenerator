from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


#This file contains the models for the database that are not default models in django (i.e. Users)
#The classes have to be in order. The reason is that you might try to make a foreign key on a class that does not exist yet.

class Topic(models.Model):
    topic = models.CharField(max_length=200)                  #Name of the topic.
    def __str__(self):                                        #Makes it so that self.topic shows up instead of topic(object)
        return self.topic

    def clean(self):                                          #Removes trailing whitespace from topic
        if self.topic:
            self.topic = self.topic.strip()
class TemplateType(models.Model):
    type = models.CharField(max_length=200)
    def __str__(self):
        return self.type
    def clean(self):                                          #Removes trailing whitespace
        if self.type:
            self.type = self.type.strip()

valid_choices = (
    (True, 'Valid'),
    (False, 'Invalid')
)

class Template(models.Model):
    question_text = models.CharField(max_length=200)          #The template. Math expression or text question ex. "Solve: ax = b + cx"
    solution = models.CharField(max_length=10000)            #Step by step solution to the answer
    answer = models.CharField(max_length=200)                 #A simple math operation to calculate the problem template. Should be the last step in the solution.
    creator = models.ForeignKey(User, blank=True, null=True)             #User ID of creator of template
    creation_date = models.DateTimeField('date created', blank=True, null=True)      #Date and time of creation
    rating = models.PositiveSmallIntegerField(blank=True, null=True)     #Difficulty rating. Defaults to 1200.
    times_solved = models.PositiveIntegerField(blank=True, null=True)    #Amount of times the problem has been solved.
    times_failed = models.PositiveIntegerField(blank=True, null=True)    #Amount of times the problem has not been solved (wrong answer.)
    topic = models.ForeignKey(Topic)                          #ID of the topic this problem belongs to ex. 2 (where 2 means algebra.)
    number_of_decimals = models.PositiveSmallIntegerField()   #The number of decimals allowed in the answer.
    answer_can_be_zero = models.BooleanField(default=False)   #True/False for if the answer to a question can be Zero.
    random_domain = models.CharField(max_length=250)           #Space separated string with 2 numbers denoting which values the random numbers can be.
    type = models.CharField(max_length=200) #this will be redundant
    choices = models.CharField(max_length=700, blank=True, null=True) #Different choices for multiple choice, empty for normal templates
    dictionary = models.CharField(max_length=10000, blank=True, null=True, default="")
    conditions = models.CharField(max_length=10000, blank=True, null=True, default="")
    fill_in = models.CharField(max_length=10000, blank=True, null=True, default="")
    valid_flag = models.BooleanField(default=False, choices=valid_choices)
    #todo: remove answer can be zero as that can be implemented in conditions using ans != 0.
    #todo: also remove number of decimals
    ##Also save the original latex for post-back:
    ##no longer needed, only calculation references are.. todo: remove unnecessary fields.
    question_text_latex = models.CharField(max_length=200, blank=True, null=True)
    solution_latex =  models.CharField(max_length=10000, blank=True, null=True)
    answer_latex = models.CharField(max_length=200, blank=True, null=True)
    choices_latex = models.CharField(max_length=700, blank=True, null=True)
    conditions_latex = models.CharField(max_length=10000, blank=True, null=True, default="")
    fill_in_latex = models.CharField(max_length=10000, blank=True, null=True, default="")
    calculation_ref = models.CharField(max_length=1000, blank=True, null=True)
    unchanged_ref = models.CharField(max_length=1000, blank=True, null=True)

    multiple_support = models.BooleanField(default=False) #Denotes whether the template supports multiple choice
    fill_in_support = multiple = models.BooleanField(default=False) #Denotes whether the template supports fill in the blanks




    def __str__(self):                                        #Makes it so that self.question_text shows up instead of topic(object)
        return self.question_text

    #todo add random_domain to each individual random variable, yo.
