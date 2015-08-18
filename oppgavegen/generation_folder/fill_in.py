from oppgavegen.utility.decorators import Debugger
from oppgavegen.utility.human_sort import human_sort


@Debugger
def fill_in_the_blanks(fill_in):
    """Returns a fill in the blank template and the position of the holes."""
    hole_dict = find_holes(fill_in)
    make_holes_dict = make_holes(hole_dict, fill_in)
    hole_positions = list(hole_dict.keys())
    hole_positions = array_to_string(hole_positions)
    fill_in = make_holes_dict['fill_in']
    return_dict = {'fill_in': fill_in, 'hole_positions': hole_positions}
    return return_dict


@Debugger
def find_holes(fill_in):
    """Finds the available holes in the template and their position."""
    # fill_in = fill_in.split('§')  # Makes fill in into a list.
    # fill_in = fill_in[len(fill_in)-1]
    hole_dict = {}  # Keeps track of what is getting replaced and the position of that in the string.
    recorder = False
    counter = 0  # Keeps track of how far in the string the loop is
    start_point = 0  # Start point of box
    a = b = c = d = e = s = ''  # Used to keep track of the last 5 variables iterated over.
    # Note: it might be faster/better to use a counter instead of storing previous characters in the for loop.
    # ie. for x in range(0, len(fill_in). See latex_to_sympy for this in action.
    for f in fill_in:
        if a == '@' and b == 'x' and c == 'x' and d == 'x' and e == 'x' and f == '@':
            recorder = not recorder  # Flip recorder
            if recorder:
                counter -= 6  # Sets the counter back 6 to compensate for @xxxx@ which is not in the original string
                start_point = counter+1
                if counter < len(fill_in):
                    if fill_in[counter] == '{' or fill_in[counter] == '(':
                        # This is to avoid a bug where } gets added, but not {
                        # However it creates another bug where ^{@xxxx@1@xxxx@} -> {1 which is fixed later
                        start_point = counter
            elif not recorder:
                end_point = counter-5
                # Swapping
                # Hole_dict[s[:-5]] = str(start_point) + ' ' + str(end_point-5)
                dict_value = s[:-5]
                if (end_point - start_point) == len(dict_value)+1:
                    start_point += 1  # Fix for the {1 bug mentioned in a earlier comment.
                dict_key = str(start_point) + ' ' + str(end_point)
                hole_dict[dict_key] = dict_value

                counter -= 6  # Sets the counter back 6 to compensate for @xxxx@ which is not in the original string
            s = ''
        elif recorder is True:
            s += f
        counter += 1
        a = b
        b = c
        c = d
        d = e
        e = f
    print(hole_dict)
    return hole_dict


@Debugger
def make_holes(hole_dict, fill_in):
    """Inserts holes at given places in the template for fill in the blanks

    :param hole_dict: dictionary of the holes to replace.
    :param fill_in: the template.
    :return: dictionary with fill in the blanks template with holes and which holes were replaced.
    """
    holes_to_replace = list(hole_dict.values())
    for s in holes_to_replace:
        fill_in = fill_in.replace('@xxxx@'+s, '\\MathQuillMathField{}'+'@xxxx@')
    fill_in = fill_in.replace('@xxxx@', '')
    return_dict = {'fill_in': fill_in, 'holes_replaced': holes_to_replace}
    return return_dict


@Debugger
def array_to_string(array):
    """Turns a array into a string separated by §."""
    string = ''
    for s in array:
        string += '§' + s
    return string[1:]  # Use [1:] to remove unnecessary § from the start


@Debugger
def get_values_from_position(position_string, solution):
    """Takes a string of positions and returns a values from the string with those positions"""
    position_array = position_string.split('§')
    values = ''
    human_sort(position_array)
    for s in position_array:
        positions = s.split()
        values += '§' + (solution[int(positions[0]):int(positions[1])])
    print('values after values are gotten from position')
    print(values)
    return values[1:]


def get_fillin_answers():
    pass