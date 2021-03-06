# Tests
from django.test import TestCase
from django.core import management

from oppgavegen.generation_folder.generation import *
from oppgavegen.parsing.latex_translator import *
from oppgavegen.utility.utility import *
from oppgavegen.generation_folder.fill_in import *
from oppgavegen.generation_folder.template_validation import *
from oppgavegen.generation_folder.calculate_parse_solution import *


def setup():
        management.call_command('loaddata', 'initial_data.json', verbosity=0)

def teardown():
        management.call_command('flush', verbosity=0, interactive=False)

class TestTemplate:
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

class TemplateGenerationTest(TestCase):
    fixtures =  ['initial_data.json']

    template1 = TestTemplate(question_text='\\text{hva er} R1R + R2R', answer='R1R+R2R',
                              solution='\\text{Adderer regnestykket:} \\n R1R+R2R = @?R1R+R2R?@',
                              rating=1200, fill_rating=1150, choice_rating=1100, topic='aritmetikk',
                              choices='@?(R0R+R1R)?@-1§@?(R0R+R1R)?@-2§@?(R0R+R1R)?@+1',
                              fill_in='\\text{Legger sammen slik} R0R+@xxxx@R1R@xxxx@=@?(R0R+R1R)?@',
                              random_domain='1 10 0§1 10 0')

    def test_calculate_answer(self):
        """
        calculate_answer() should return a calculated version of the input string.
        The function also rounds the answer according to domain using round_answer()
        """
        r_domain1 = json.dumps({'R1R' : [[0, 0 , 0], False]})
        r_domain2 = json.dumps({'R1R' : [[0, 0 , 2], False]})
        r_domain3 = json.dumps({'R1R' : [[0, 0 , 0], False]})
        self.assertEqual(calculate_answer(1+1, r_domain1), '2')
        self.assertEqual(calculate_answer(1.25+1, r_domain2), '2.25')
        self.assertEqual(calculate_answer(1.50+1.50, r_domain3), '3') #check to se if 3.00 gets converted to 3.

    def test_round_answer(self):
        """
        round_answer() rounds a number according to domain
        """
        self.assertEqual(round_answer({'R1R' : [[0, 0 , 0], False]}, 1.25), 1)
        self.assertEqual(round_answer({'R1R' : [[0, 0 , 1], False]}, 1.25), 1.3)
        self.assertEqual(round_answer({'R1R' : [[0, 0 , 2], False]}, 1.25), 1.25)

    def test_parse_solution(self):
        """
        Checks if parse_solution works properly by parsing/calculating text between @? and ?@
        """
        self.assertEqual(parse_solution('teststring @?2+2?@ and @?2+3?@', self.template1.random_domain),
                         'teststring (4) and (5)')

    def test_replace_words(self):
        """
        Checks if words get replaced correctly
        """
        dict = replace_words('testsentence', 'testsentence§new testsentence')
        self.assertEqual(dict['sentence'], 'new testsentence')
        self.assertEqual(dict['replace_string'], 'testsentence§new testsentence')


    def test_calculate_array(self):
        self.assertEqual(calculate_array(['2+2','3+3'], self.template1.random_domain), ['4', '6'])

    def test_after_equal_sign(self):
        self.assertEqual(after_equal_sign('x=2'),'2')

    def test_replace_variables_from_array(self):
        test_string = replace_variables_from_array(['R1R', '1', 'R2R', '2'], self.template1.question_text)
        self.assertEqual(test_string, '\\text{hva er} (1) + (2)')

    def test_parse_answer(self):
        self.assertEqual(parse_answer('@?1+1?@§@?1+2?@', self.template1.random_domain), '(2)§(3)')

    def test_dict_to_string(self):
        dict = {'R1R' : '1', 'R2R' : '2'}
        string = dict_to_string(dict)
        if string == 'R2R§2§R1R§1':
            string = 'R1R§1§R2R§2'
        # This is done because dicts aren't sorted, the order is arbitrary.
        # The function (dict_to_string) doesn't sort the dicts as that is
        # redundant and would result in performance loss.
        self.assertEqual(string, 'R1R§1§R2R§2')

    def test_array_to_string(self):
        arr = ['R1R', 'R2R']
        string = array_to_string(arr)
        self.assertEqual(string, 'R1R§R2R')

    def test_remove_unnecessary(self):
        string = '@?test?@'
        self.assertEqual(remove_unnecessary(string), 'test')

    def test_string_replace(self):
        dict = {'R1R' : '1', 'R2R' : '2'}
        string = self.template1.answer
        self.assertEqual(string_replace(string,dict),'(1)+(2)')

    def test_is_number(self):
        self.assertEqual(is_number('test'), False)
        self.assertEqual(is_number('2'),True)
        self.assertEqual(is_number(2),True)
        self.assertEqual(is_number(2.15),True)

    def test_make_number(self):
        domain1 = [1, 1, 0]
        domain2 = [1.25, 1.25, 1]
        domain3 = [1.25, 1.25, 2]
        self.assertEqual(make_number(domain1),1)
        self.assertEqual(make_number(domain2),1.2) #the reason this is 1.2 is bankers rounding.
        self.assertEqual(make_number(domain3),1.25)

    def test_check_conditions(self):
        pass

    def test_new_random_value(self):
        domain_dict = {'R1R' : [1, 1, 0], 'R2R' : [0, 10, 0]}
        self.assertEqual(new_random_value('R1R', domain_dict),1)

    def test_make_holes(self):
        correct = {'holes_replaced': ['R1R'],
                   'fill_in': '\\text{Legger sammen slik} R0R+\\MathQuillMathField{}=@?(R0R+R1R)?@'}
        self.assertEqual(make_holes({'31 34': 'R1R'}, self.template1.fill_in), correct)

    def test_find_holes(self):
        self.assertEqual(find_holes(self.template1.fill_in), {'30 33': 'R1R'})

    def test_fill_in_the_blanks(self):
        correct_dict = {'hole_positions': '30 33',
                        'fill_in': '\\text{Legger sammen slik} R0R+\\MathQuillMathField{}=@?(R0R+R1R)?@'}
        test2 = "f'\left(x\\right)=\\frac{d}{dx}\left(R0Rx^{R1R}+R2Rx^{@xxxx@1@xxxx@}-R6R\\right)=@xxxx@R1R@xxxx@" \
                "\cdot R0Rx^{R1R-@xxxx@1@xxxx@}+@xxxx@1@xxxx@\cdot R2Rx^{1-@xxxx@1@xxxx@}-@xxxx@0@xxxx@" \
                "§f'\left(x\\right)=@xxxx@@?(R0R\cdot   R1R)?@@xxxx@x^@xxxx@{@?(R1R-1)?@}@xxxx@+@xxxx@R2R@xxxx@"

        correct_dict2 = {'hole_positions' : '',
                         'fill_in': "f'\left(x\\right)=\\frac{d}{dx}\left(R0Rx^{R1R}+R2Rx^MathQuillMathField{}-R6R"
                                    "\\right)=MathQuillMathField{}\cdot R0Rx^{R1R-MathQuillMathField{}}+"
                                    "MathQuillMathField{}\cdot "
                                    "R2Rx^{1-MathQuillMathField{}}-MathQuillMathField{}§f'\left(x\\right)="
                                    "MathQuillMathField{}xMathQuillMathField{}+MathQuillMathField{}"}
        self.assertEqual(fill_in_the_blanks(self.template1.fill_in), correct_dict)


    def test_get_values_from_position(self):
        self.assertEqual(get_values_from_position('32 35', self.template1.solution), 'R1R')

    def test_get_question(self):
        #user = User.objects.get(pk=1)
        #question = get_question(user, 1)
        #self.assertEqual(question, Template.objects.get(pk=1))
        pass

class LatexTranslatorTest(TestCase):

    def test_latex_to_sympy(self):
        string1 = '\\frac{\\sqrt{1}}{\\frac{2}{3}\cdot4}'
        self.assertEqual(latex_to_sympy(string1),'(sqrt(1))/((2)/(3)*4) ')

    def test_find_indexes(self):
        test_string1 = '\\begin{pmatrix}1&2\\\\3&4\\\\5&6\\end{pmatrix} test ' \
                       '\\begin{pmatrix}7&8\\\\9&10\\\\11&12\\end{pmatrix}'
        index1 = '\\begin{pmatrix}'

        self.assertEqual(find_indexes(test_string1, index1), [0, 47])

    def test_sort_nesting(self):
        list1 = [1, 2, 3]
        list2 = [8, 9, 10]

        self.assertEqual(sort_nesting(list1, list2), [10,9,8])

    def test_pmatrix_to_matrix(self):
        test_string1 = '\\begin(pmatrix)1&2\\\\3&4\\\\5&6\\end(pmatrix) test ' \
                       '\\begin(pmatrix)7&8\\\\9&10\\\\11&12\\end(pmatrix)'
        correct_string = ' Matrix([[1, 2], [3, 4], [5, 6]])  test  Matrix([[7, 8], [9, 10], [11, 12]]) '

        self.assertEqual(pmatrix_to_matrix(test_string1), correct_string)

class ViewLogicTest(TestCase):
    pass

