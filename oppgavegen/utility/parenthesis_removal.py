
def parenthesis_remover(s):
    """removes parenthesises from expressions and checks if the expression is still valid."""
    pairs = find_pairs(s, '(', ')')
    for pair in pairs:
        pass






def find_pairs(s, one, two):
    """
    :param string: The string to look for pairs in.
    :param one: The first of a pair.
    :param two: The second of a pair.
    :return: returns a list of pairs.
    """
    counter = 0
    pairs = []
    print(s)
    for i in range(0, len(s)):
        if s[i] == one:
            for j in range(i+1, len(s)):
                print(counter)
                if s[j] == two and counter == 0:
                    pairs.append([i, j])
                    counter = 0
                    break
                if s[j] == one:
                   counter += 1
                elif s[j] == two:
                    counter -= 1
    return pairs

    # while i < len(s):  # Logic for inserting a / in fractals
    #     if s[i] == 'c' and s[i-1] == 'a' and s[i-2] == 'r' and s[i-3] == 'f' and s[i-4] == '\\':
    #         recorder = True
    #     if recorder:
    #         if s[i] == '(':
    #             counter += 1
    #         elif s[i] == ')':
    #             counter -= 1
    #         if s[i] == ')' and counter == 0:
    #             s = s[0:i+1] + "/" + s[i+1:len(s)]
    #             recorder = False
    #     i += 1
