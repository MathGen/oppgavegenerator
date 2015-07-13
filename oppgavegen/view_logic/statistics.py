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
        count = templates.filter(rating__range=(min, max)).count()
        count += templates.filter(fill_rating__range=(min, max)).count()
        count += templates.filter(choice_rating__range=(min, max)).count()
        morrisdata.append('{rating: "%d-%d", oppgaver: %d },' % (min, max, count))
        min += interval
        max += interval

    # Check for entries in higher cutoff range (from endintervals to cutoffmax)
    if templates.filter(rating__range=(endintervals, cutoffmax)):
        count = templates.filter(level_rating__range=(endintervals,cutoffmax)).count()
        count += templates.filter(fill_rating__range=(endintervals, cutoffmax)).count()
        count += templates.filter(choice_rating__range=(endintervals, cutoffmax)).count()
        morrisdata.append('{rating: "%d-%d", oppgaver: %d },' % (endintervals, cutoffmax, count))

    return morrisdata