from oppgavegen.view_logic.progress import *
from oppgavegen.models import Set, Chapter

# NOTE: in the test version the database used is sql lite. In sql lite the between statement is inclusive
# this means range(1, 10) would return all int numbers between 0 and 11.
# if the database is changed to another, check how the between statement for that database works
# if the between statement of the new database is not inclusive this logic in this file would have to change a bit.
# The change would be to subtract 1 from lower bound and add 1 to upper bound and also change the string values.
# note: postgresql also uses inclusive between.


def get_level_student_statistics(level, start_interval=1100, end_interval=2300, interval=100,
                                 cutoff_min=800, cutoff_max=2400):
    morris_data = []
    students = level.student_progresses.all()
    intervals = int((end_interval-start_interval)/interval)

    # Check for and count entries in lower cutoff range (from 0 to cutoff_min)
    if students.filter(level_rating__range=(0, cutoff_min-1)):
        count = students.filter(level_rating__range=(0, cutoff_min-1)).count()
        morris_data.append('{rating: "0-%d", studenter: %d },' % (cutoff_min-1, count))

    # Check for and count entries between lower cutoff and start_interval
    if students.filter(level_rating__range=(cutoff_min, start_interval-1)):
        count = students.filter(level_rating__range=(cutoff_min, start_interval-1)).count()
        morris_data.append('{rating: "%d-%d", studenter: %d },' % (cutoff_min, start_interval-1, count))

    # Count entries in standard range (start_intervals to end_intervals)
    lower_bound = start_interval
    upper_bound = start_interval+interval-1
    print(upper_bound)
    for i in range(intervals):
        count = students.filter(level_rating__range=(lower_bound, upper_bound)).count()
        morris_data.append('{rating: "%d-%d", studenter: %d },' % (lower_bound, upper_bound, count))
        lower_bound+=interval
        upper_bound+=interval

    # Check for and count entries in higher cutoff range (from end_intervals to cutoff_max)
    if students.filter(level_rating__range=(end_interval, cutoff_max)):
        count = students.filter(level_rating__range=(end_interval,cutoff_max)).count()
        morris_data.append('{rating: "%d-%d", studenter: %d },' % (end_interval, cutoff_max, count))

    print(morris_data)
    return morris_data


def get_level_template_statistics(level, start_interval=1100, end_interval=2300, interval=100,
                                  cutoff_min=800, cutoff_max=2400):
    morris_data = []
    templates = level.templates.all()
    num_intervals = int((end_interval-start_interval)/interval)

    # Check for entries in lower cutoff range (from 0 to cutoffmin)
    if templates.filter(rating__range=(0, cutoff_min-1)):
        count = templates.filter(rating__range=(0, cutoff_min-1)).count()
        count += templates.filter(fill_rating__range=(0, cutoff_min-1)).count()
        count += templates.filter(choice_rating__range=(0, cutoff_min-1)).count()

        morris_data.append('{rating: "0-%d", oppgaver: %d },' % (cutoff_min-1, count))

    # Check for entries between lower cutoff to start_interval
    if templates.filter(rating__range=(cutoff_min, start_interval-1)):
        count = templates.filter(rating__range=(cutoff_min, start_interval-1)).count()
        count += templates.filter(fill_rating__range=(cutoff_min, start_interval-1)).count()
        count += templates.filter(choice_rating__range=(cutoff_min, start_interval-1)).count()

        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (cutoff_min, start_interval-1 , count))

    # Check for entries in standard range (start_interval to end_interval)
    lower_bound = start_interval
    upper_bound = lower_bound+interval-1
    for i in range(num_intervals):
        count = templates.filter(rating__range=(lower_bound, upper_bound)).count()
        count += templates.filter(fill_rating__range=(lower_bound, upper_bound)).count()
        count += templates.filter(choice_rating__range=(lower_bound, upper_bound)).count()
        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (lower_bound, upper_bound, count))
        lower_bound += interval
        upper_bound += interval

    # Check for entries in higher cutoff range (from endintervals to cutoffmax)
    if templates.filter(rating__range=(end_interval, cutoff_max)):
        count = templates.filter(level_rating__range=(end_interval,cutoff_max)).count()
        count += templates.filter(fill_rating__range=(end_interval, cutoff_max)).filter(fill_in_support=True).count()
        count += templates.filter(choice_rating__range=(end_interval, cutoff_max)).filter(multiple_support=True).count()
        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (end_interval, cutoff_max, count))

    return morris_data


def get_level_template_original_statistics(level, interval=100):
    """Gets the original rating of templates in a level, only works for rating intervals dividable by 50"""
    morris_data = []
    templates = level.templates.all()
    interval /=  50
    lower_bound = 1  # Difficulty starts at 1 and ends at 25
    upper_bound = interval
    # Since range in used +- 1 is needed on the bounds, ie. to get 1 and 2 the range is 0,3
    while lower_bound < 25:  # as of the making of this 25 is the max difficulty number
        count = templates.filter(difficulty__range=(lower_bound, upper_bound)).count()
        count += templates.filter(difficulty_multiple__range=(lower_bound, upper_bound)).filter(fill_in_support=True).count()
        count += templates.filter(difficulty_blanks__range=(lower_bound, upper_bound)).filter(multiple_support=True).count()
        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (lower_bound*50+950, upper_bound*50+950, count))
        lower_bound += interval
        upper_bound += interval

    return morris_data

def user_stats_for_set(user, set_id):
    set = Set.objects.get(pk=set_id)
    chapters = set.chapters.all()
    chapter_status_dict = {}
    for chapter in chapters:
        chapter_status_dict[chapter.name] = check_for_chapter_completed(user, chapter)

    return chapter_status_dict

def stats_for_set(set_id):
    """Returns the stats for all users in a set on the form {'name': {'chapter': progress,..},..}"""
    set = Set.objects.get(pk=set_id)
    users = set.users.all()
    stats = {}
    for user in users:
        stats[user.first_name + ' ' + user.last_name] = user_stats_for_set(user, set_id)

    order = Set.order.split(',')
    header = ['Navn']
    for x in order:
        chapter = Chapter.objects.get(pk=x)
        header.append(chapter.name)
    return (header,stats)  # Todo: put into table and display.

