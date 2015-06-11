# Tests
from django.test import TestCase
from oppgavegen.generation import *

class testTemplate:

    def __init__(self, question_text, solution, answer, rating, fill_rating, choice_rating, topic, random_domain,
                 choices='', dictionary='', conditions='', fill_in=''):
        self.question_text = question_text
        self.solution = solution
        self.answer = answer
        self.rating = rating
        self.fill_rating = fill_rating
        self.choice_rating = choice_rating
        self.topic = topic
        self.random_domain = random_domain
        self.choices = choices
        self.dictionary = dictionary
        self.conditions = conditions
        self.fill_in = fill_in

    # def question_text(self):
    #     return self.__question_text
    #
    # def solution(self):
    #     return self.__solution
    #
    # def answer(self):
    #     return self.__answer
    #
    # def rating(self):
    #     return self.__rating
    #
    # def fill_rating(self):
    #     return self.__fill_in_rating
    #
    # def choice_rating(self):
    #     return self.__choice_rating
    #
    # def topic(self):
    #     return self.__topic
    #
    # def random_domain(self):
    #     return self.__random_domain
    #
    # def choices(self):
    #     return self.__choices
    #
    # def dictionary(self):
    #     return self.__dictionary
    #
    # def conditions(self):
    #     return self.__conditions
    #
    # def fill_in(self):
    #     return self.__fill_in

class templateGenerationTest(TestCase):
    template1 = testTemplate(question_text='\\text{hva er R1R + R2R}', answer='R1R+R2R',
                              solution='\\text{Adderer regnestykket:} \\n R1R+R2R = @?R1R+R2R?@',
                              rating=1200, fill_rating=1150, choice_rating=1100, topic='aritmetikk',
                              choices='@?(R0R+R1R)?@-1§@?(R0R+R1R)?@-2§@?(R0R+R1R)?@+1',
                              fill_in='\\text{Legger sammen slik}\\nR0R+@xxxx@R1R@xxxx@=@?(R0R+R1R)?@',
                              random_domain='1 10 0§1 10 0')

    def test_calculate_answer(self):
        """
        calculate_answer() should return a calculated version of the input string.
        The function also rounds the answer according to domain using round_answer()
        """
        self.assertEqual(calculate_answer('1+1', self.template1.random_domain), 2)

    def test_round_answer(self):
        """
        round_answer() rounds a number according to domain
        """
        self.assertEqual(calculate_answer('1.25', '2 5 0'), 1)
        self.assertEqual(calculate_answer('1.25', '2 5 1'), 1.3)
        self.assertEqual(calculate_answer('1.25', '2 5 2'), 1.25)