from oppgavegen.decorators import Debugger
from random import randint


@Debugger
def after_equal_sign(s):
    """Returns everything after the last '=' sign of a string."""
    if '=' in s:
        s = s.split("=")
        s = s[len(s)-1]
    return s


@Debugger
def replace_words(sentence, dictionary):
    """
    Replaces variables in a string with the value of a key in the given dictionary.
    Example: ('example sentence', 'example § apple, grape') ->
             {'sentence': 'apple sentence', 'replace_string' 'example § apple'}}
    :param sentence: String to replace words in.
    :param dictionary: A splittable (§) string with word alternatives.
    :return: dictionary with the new sentence and a splittable string with what words were replaced
    """
    dictionary = dictionary.split('§')
    replace_string = ''
    for i in range(0, len(dictionary)-1, 2):
        replace_strings = dictionary[i+1].split(',')
        replace_word = replace_strings[randint(0, len(replace_strings)-1)]
        sentence = sentence.replace(dictionary[i], replace_word)
        replace_string += '§' + dictionary[i] + '§' + replace_word
    return {'sentence': sentence, 'replace_string': replace_string[1:]}


@Debugger
def is_number(s):
    """Returns whether a string is a number or not."""
    try:
        float(s)
        return True
    except ValueError:
        return False


@Debugger
def remove_unnecessary(string):
    """Removes unnecessary symbols from a string and returns the string."""
    string = string.replace('@?', '')
    string = string.replace('?@', '')
    return string


@Debugger
def dict_to_string(variable_dict):
    """Returns a separated string of the key and value pairs of a dict"""
    variables_used = ""
    for key in variable_dict:
        variables_used += '§' + str(key) + '§' + str(variable_dict[key])
    return variables_used[1:]  # Use [1:] to remove unnecessary § from the start


@Debugger
def array_to_string(array):
    """Turns a array into a string separated by §."""
    string = ''
    for s in array:
        string += '§' + s
    return string[1:]  # Use [1:] to remove unnecessary § from the start

@Debugger
def string_replace(string, variable_dict):
    """Replaces variables in a string with numbers from a dict

    :param string: String with variables in it.
    :param variable_dict: a dictionary with variable names as keys and the number to replace them which as values.
    :return: String with numbers instead of variable names.
    """
    for key in variable_dict:
        string = string.replace(key, str(variable_dict[key]))
    return string

@Debugger
def replace_variables_from_array(arr, s):
    """Takes a string and replaces variables in the string with ones from the array

    #Example: (['R10', '5', 'R1', '7'], 'example string R1 and R10') -> 'example string 7 and 5'
    :param arr: Array of variables
    :param s: String to replace variables in
    :return: String with replaced variables
    """
    for x in range(0, len(arr)-1, 2):  # Set increment size to 2.
        s = s.replace(arr[x], arr[x+1])
    return s