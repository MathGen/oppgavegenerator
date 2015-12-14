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


def get_level_template_statistics(level, offset, start_interval=1100, end_interval=2300, interval=100,
                                  cutoff_min=800, cutoff_max=2400):
    morris_data = []
    templates = level.templates.all().values('rating','fill_rating','choice_rating')
    #add level offset to all template ratings
    for template in templates:
        template['rating'] += offset
        template['fill_rating'] += offset
        template['choice_rating'] += offset

    num_intervals = int((end_interval-start_interval)/interval)

    # Check for entries in lower cutoff range (from 0 to cutoffmin)
    if templates.filter(rating__range=(0, cutoff_min-1)) \
    or templates.filter(fill_rating__range=(0,cutoff_min-1)) \
    or templates.filter(choice_rating__range=(0,cutoff_min-1)):
        count = templates.filter(rating__range=(0, cutoff_min-1)).count()
        count += templates.filter(fill_in_support=True,fill_rating__range=(0, cutoff_min-1)).count()
        count += templates.filter(multiple_support=True,choice_rating__range=(0, cutoff_min-1)).count()

        morris_data.append('{rating: "0-%d", oppgaver: %d },' % (cutoff_min-1, count))

    # Check for entries between lower cutoff to start_interval
    if templates.filter(rating__range=(cutoff_min, start_interval-1)) \
    or templates.filter(fill_rating__range=(cutoff_min,start_interval-1)) \
    or templates.filter(choice_rating__range=(cutoff_min,start_interval-1)):
        count = templates.filter(rating__range=(cutoff_min, start_interval-1)).count()
        count += templates.filter(fill_in_support=True,fill_rating__range=(cutoff_min, start_interval-1)).count()
        count += templates.filter(multiple_support=True,choice_rating__range=(cutoff_min, start_interval-1)).count()

        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (cutoff_min, start_interval-1 , count))

    # Count entries in standard range (start_interval to end_interval)
    lower_bound = start_interval
    upper_bound = lower_bound+interval-1
    for i in range(num_intervals):
        count = templates.filter(rating__range=(lower_bound, upper_bound)).count()
        count += templates.filter(fill_in_support=True,fill_rating__range=(lower_bound, upper_bound)).count()
        count += templates.filter(multiple_support=True,choice_rating__range=(lower_bound, upper_bound)).count()
        morris_data.append('{rating: "%d-%d", oppgaver: %d },' % (lower_bound, upper_bound, count))
        lower_bound += interval
        upper_bound += interval

    # Check for entries in higher cutoff range (from endintervals to cutoffmax)
    if templates.filter(rating__range=(end_interval, cutoff_max)) \
    or templates.filter(fill_rating__range=(end_interval,cutoff_max)) \
    or templates.filter(choice_rating__range=(end_interval,cutoff_max)):
        count = templates.filter(level_rating__range=(end_interval,cutoff_max)).count()
        count += templates.filter(fill_in_support=True,fill_rating__range=(end_interval, cutoff_max)).count()
        count += templates.filter(multiple_support=True,choice_rating__range=(end_interval, cutoff_max)).count()
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
    """returns whether a user has completed the chapters in a set (according to order)"""
    set = Set.objects.get(pk=set_id)
    order = set.order.split(',')
    chapter_status_list = []
    for c_id in order:
        c_id = int(c_id)
        chapter = Chapter.objects.get(pk=c_id)
        chapter_status_list.append(check_chapter_completion(user, chapter))

    return chapter_status_list


def stats_for_set(set_id):
    """Returns the stats for all users in a set on the form {'name': [progress1, progress2],..}"""
    set = Set.objects.get(pk=set_id)
    users = set.users.all().order_by('last_name')
    stats = []
    print('1')
    for user in users:
        stats.append([user.first_name + ' ' + user.last_name] + user_stats_for_set(user, set_id))

    headers = ['Student']
    order = set.order
    order = order.split(',')
    for x in order:
        x = int(x)
        chapter = Chapter.objects.get(pk=x)
        headers.append('<a href="/chapter/%d/stats">%s</a>' % (chapter.id, chapter.name)) # clickable chapter names
    return headers, stats                                                                 # links to chapter details


def stats_for_chapter_levels(chapter_id):
    """
    Return a list of level names in a chapter and a list of students and their progress for all
    levels in requirement chapter. The data is meant to be displayed in a table.
    Since there's a unique entry for every student->level match we first need to create a clean list of users
    from the associated UserLevelProgress-entries for all the levels in a chapter, and then extract the score for
    every progress-entry that belongs that user. If a student skips a level it will leave a gap in the table
    and put the score of the next level in the place of the skipped level.
    """

    # get all levels by filtering over chapter relation. this doesn't get them in the right order as defined in the
    # chapter.order field but saves on needed queries
    levels = Level.objects.filter(chapters__id=chapter_id).order_by('pk').prefetch_related('student_progresses')
    userscores = (l.student_progresses.all().select_related('user') for l in levels) # creates list of scores in list of levels
    all_users = []
    stats = []
    for u in userscores:
        for n in u:
            all_users.append(n.user)
    users = sorted(list(set(all_users)), key=lambda user: user.last_name) # remove duplicates and sort by last name
    headers = ['Student']
    for level in levels:
        headers.append(level.name)
    for user in users:
        stats.append([user.get_full_name()] + user_scores_for_levels(user, levels))

    return headers, stats

def user_scores_for_levels(user, levels):
    """
    Filter one users scores from list of levels.
    If a user hasn't started a level yet, add "0" as a record.
    """
    userscores = []


    for level in levels:
        scores = []
        # If there's no userprogress-entry for a given level, add a 0 to the scorelist
        if not level.student_progresses.filter(user=user,level_id=level.id).exists():
            scores.append(0)
        else:
            scores.append(level.student_progresses.get(user=user,level_id=level.id))
        for score in scores:
            # no entry means 0 score/stars
            if score == 0:
                userscores.append(0)
            else:
                userscores.append(int(score.stars))
    return userscores
