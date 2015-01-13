from random import randint


def printer():
    string = "Spaghetti"
    return string

def arithmetics():
    number1 = randint(0,10)
    number2 = randint(0,10)
    operators = ["+", "-", "*"]
    opNumber = randint(0,2)
    if opNumber == 0:
        answer = number1 + number2
    elif opNumber == 1:
        answer = number1 - number2
    else:
        answer = number1 * number2
    arr = [number1,number2,answer, operators[opNumber]]
    return arr

def algebra():
    # 2x + 4 = 10
    # x = 3
    # nx + a = b

    x = randint(0,6)
    n = randint(1,3)
    a = randint(0,10)
    operators = ["+", "-"]
    opNumber = randint(0,1)
    if opNumber == 0:
        b = (n*x)+a
    else:
        b = (n*x)-a
    arr = [x, n, a, b, operators[opNumber]]
    return arr