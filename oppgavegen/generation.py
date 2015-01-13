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

def algebra2():
    x = randint(0,6)
    a = randint(1,10)
    b = randint(1,10)
    c = randint(1,10)
    d = randint(1,10)
    n = randint(1,3)



