from oppgavegen.models import Level

def get_level_student_statistics(level, startintervals=1100, endintervals=2300, interval=100,
                                 cutoffmin=800, cutoffmax=2400):
    morrisdata = []
    students = level.student_progresses.all()
    intervals = int((endintervals-startintervals)/interval)

    # Check for entries in lower cutoff range (from 0 to cutoffmin)
    if students.filter(level_rating__range=(0, cutoffmin)):
        count = students.filter(level_rating__range=(0, cutoffmin)).count()
        morrisdata.append('{rating: "0-%d", studenter: %d },' % (cutoffmin, count))

    # Check for entries in standard range (startintervals to endintervals)
    min = startintervals
    max = min+interval
    for i in range(intervals):
        count = students.filter(level_rating__range=(min, max)).count()
        morrisdata.append('{rating: "%d-%d", studenter: %d },' % (min, max, count))
        min+=interval
        max+=interval

    # Check for entries in higher cutoff range (from endintervals to cutoffmax)
    if students.filter(level_rating__range=(endintervals, cutoffmax)):
        count = students.filter(level_rating__range=(endintervals,cutoffmax)).count()
        morrisdata.append('{rating: "%d-%d", studenter: %d },' % (endintervals, cutoffmax, count))

    return morrisdata

def get_level_template_statistics(level, startintervals=1100, endintervals=2300, interval=100,
                                 cutoffmin=800, cutoffmax=2400):
    morrisdata = []
    templates = level.templates.all()
    intervals = int((endintervals-startintervals)/interval)

    # Check for entries in lower cutoff range (from 0 to cutoffmin)
    if templates.filter(rating__range=(0, cutoffmin)):
        count = templates.filter(rating__range=(0, cutoffmin)).count()
        count += templates.filter(fill_rating__range=(0, cutoffmin)).count()
        count += templates.filter(choice_rating__range=(0, cutoffmin)).count()

        morrisdata.append('{rating: "0-%d", oppgaver: %d },' % (cutoffmin, count))

    # Check for entries in standard range (startintervals to endintervals)
    min = startintervals
    max = min+interval
    for i in range(intervals):
        count = templates.filter(rating__range=(min-1, max)).count()
        count += templates.filter(fill_rating__range=(min-1, max)).count()
        count += templates.filter(choice_rating__range=(min-1, max)).count()
        morrisdata.append('{rating: "%d-%d", oppgaver: %d },' % (min, max, count))
        min += interval
        max += interval

    # Check for entries in higher cutoff range (from endintervals to cutoffmax)
    if templates.filter(rating__range=(endintervals-1, cutoffmax)):
        count = templates.filter(level_rating__range=(endintervals-1,cutoffmax)).count()
        count += templates.filter(fill_rating__range=(endintervals-1, cutoffmax)).count()
        count += templates.filter(choice_rating__range=(endintervals-1, cutoffmax)).count()
        morrisdata.append('{rating: "%d-%d", oppgaver: %d },' % (endintervals, cutoffmax, count))

    return morrisdata

def get_level_template_original_statistics(level, intervall=100):
    morrisdata = []
    templates = level.templates.all()
    intervall /=  50
    lower_bound = 0
    upper_bound = intervall
    while lower_bound < 25:  # as of the making of this 25 is the max difficulty number
        count = templates.filter(difficulty__range=(lower_bound, upper_bound)).count()
        count += templates.filter(difficulty_multiple__range=(lower_bound, upper_bound)).count()
        count += templates.filter(difficulty_blanks__range=(lower_bound, upper_bound)).count()
        morrisdata.append('{rating: "%d-%d", oppgaver: %d },' % (lower_bound*50+950, upper_bound*50+950, count))
        lower_bound += intervall
        upper_bound += intervall





    return morrisdata