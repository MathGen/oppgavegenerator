from oppgavegen.models import User, Level, UserLevelProgress, Chapter
import json

def calculate_progress(user, chapter):
    levels = chapter.level_order
    levels = levels.split(',')
    counter = 0
    for i in levels:
        level = Level.objects.get(pk=i)
        print(1)
        try:
            q = UserLevelProgress.objects.get(user=user, level=level)
        except UserLevelProgress.DoesNotExist:
            break
        if q.stars < 1:
            break
        counter += 1
    return counter

# avg of stars for every level in chapt.

def chapter_progress(user, set, medals, completed):
    """
    Finds the progress of a given chapter and changes the lists medals and completed to match the progress info
    :param user: the user the progress is requested for, usually request.user from view
    :param set: The set to check the users progress for
    :param medals: a list that holds the medals for the chapters in the set
    :param completed: a list that holds how many levels are completed in the chapters
    :return: No return as the return is the lists getting changed.
    """
    for i in set.chapter_order.split(','):
        level_star_count = 0
        levels_completed = 0
        level_counter = 0
        chapter = Chapter.objects.get(pk=i)
        for level in chapter.levels.all():
            level_counter += 1
            try:
                q = UserLevelProgress.objects.get(user=user, level=level)
                level_star_count += q.stars
                if q.stars > 0:
                    levels_completed += 1
            except UserLevelProgress.DoesNotExist:
                pass
        medals.append(level_star_count//level_counter)
        completed.append(levels_completed)


def get_stars_per_level(user, chapter):
    levels = chapter.level_order
    levels = levels.split(',')
    star_list = []
    for i in levels:
        level = Level.objects.get(pk=i)
        try:
            q = UserLevelProgress.objects.get(user=user, level=level)
            star_list.append(q.stars)
        except UserLevelProgress.DoesNotExist:
            star_list.append(0)
    star_list = json.dumps(star_list)
    return star_list