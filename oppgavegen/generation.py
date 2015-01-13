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
    string = "Hva er " + str(number1) + " " + operators[opNumber] + " " + str(number2) + "?"
    arr = [string, answer]
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
    string = str(n) + "x " + operators[opNumber] + " " + str(a) + " = " + str(b)
    arr = [string, x]
    return arr

def checkAnswer(user_answer, answer):
    if user_answer == answer:
       string = "Du har svart riktig!"
    else:
        string = "Du har svart feil. Svaret er: " + str(answer)

    return string

def test():
    # ax + b = c
    # ax + b = cx
    # ax + bx = c
    # a + bx = c
    # a + b = cx
    # a + bx = cx
    # a + b = c + d

    v = randint(1, 2)   # antall ledd (venstre)
    h = randint(1, 2)   # antall ledd (høyre)
    vh = 4
    a = randint(0, 8)
    b = randint(0, 8)
    c = randint(0, 8)
    x = randint(2, 6)
    number_of_x = randint(1, vh-1)
    operators = ["+", "-"]
    op_number1 = randint(0, 1)
    op_number2 = randint(0, 1)
    x_string = [" ", " ", " ", " "]
    x_placement = []
    for i in range(0, vh):
        x_placement += [1]
    if number_of_x == 1:
        i = randint(0, vh)
        x_placement[i] = x
        x_string[i] = "x "
    elif number_of_x == 2:
        pos = sample(range(0, vh), 2)
        x_placement[pos[0]] = x
        x_placement[pos[1]] = x
        x_string[pos[0]] = "x "
        x_string[pos[1]] = "x "
    else:
        pos = sample(range(0, vh), 3)
        x_placement[pos[0]] = x
        x_placement[pos[1]] = x
        x_placement[pos[2]] = x
        x_string[pos[0]] = "x "
        x_string[pos[1]] = "x "
        x_string[pos[2]] = "x "

    ax = a * x_placement[0]
    if vh == 4:
        bx = b * x_placement[1]
        cx = c * x_placement[2]
        if op_number1 == 0 and op_number2 == 0:
            dx = (ax + bx - cx) * x_placement[3]
        elif op_number1 == 0 and op_number2 == 1:
            dx = -(ax + bx - cx) * x_placement[3]
        elif op_number1 == 1 and op_number2 == 0:
            dx = (ax - bx - cx) * x_placement[3]
        else:
            dx = -(ax - bx - cx) * x_placement[3]
        d = dx / x_placement[3]
        string = str(a) + "%s" + str(operators[op_number1]) + " " + str(b) + "%s" + "= " + str(c) + "%s" + str(operators[op_number2]) + str(d) + "%s"
        s = string % (x_string[0], x_string[1], x_string[2], x_string[3])

    arr = [s, x]
    return arr



