from oppgavegen.models import User, UserLevelProgress, Level, Template, Offset
from oppgavegen.utility.decorators import Debugger


def change_elo(template, user, user_won, type):
    """Changes the elo of both user and task depending on who won."""
    u = User.objects.get(username=user.username)
    user_rating = u.extendeduser.rating
    # Formula for elo: Rx = Rx(old) + prefactor *(W-Ex) where W=1 if wins and W=0 if x loses
    # and Ex is the expected probability that x will win.
    # Ea = (1+10^((Rb-Ra)/400))^-1
    # Eb = (1+10^((Ra-Rb)/400))^-1
    if type == 'blanks':
        template_rating = template.fill_rating
    elif type == 'multiple':
        template_rating = template.choice_rating
    else:
        template_rating = template.rating

    expected_user = (1+10**((template_rating-user_rating)/400))**(-1)
    expected_template = (1+10**((template_rating-user_rating)/400))**(-1)
    prefactor_user = 32  # This value could be adjusted according to elo of the user (lower for higher ratings..)
    prefactor_template = 8  # This value could be adjusted according to elo of the user (lower for higher ratings..)

    if user_won:
        new_user_rating = user_rating + prefactor_user*(1-expected_user)
        new_template_rating = template_rating + prefactor_template*(0-expected_template)
        template.times_solved += 1
    else:
        new_user_rating = user_rating + prefactor_user*(0-expected_user)
        new_template_rating = template_rating + prefactor_template*(1-expected_template)
        template.times_failed += 1
    user.extendeduser.rating = new_user_rating
    user.extendeduser.save()
    if type == 'blanks':
        template.fill_rating = new_template_rating
    elif type == 'multiple':
        template.choice_rating = new_template_rating
    else:
        template.rating = new_template_rating
    template.save()
    return


@Debugger
def change_level_rating(template, user, user_won, type, level_id):
    """Changes the elo of both user and task depending on who won."""
    u = User.objects.get(username=user.username)
    level = Level.objects.get(pk=level_id)
    user_progress = UserLevelProgress.objects.get(user=u, level=level)
    user_rating = user_progress.level_rating
    # Formula for elo: Rx = Rx(old) + prefactor *(W-Ex) where W=1 if wins and W=0 if x loses
    # and Ex is the expected probability that x will win.
    # Ea = (1+10^((Rb-Ra)/400))^-1
    # Eb = (1+10^((Ra-Rb)/400))^-1
    if type == 'blanks':
        template_rating = template.fill_rating
    elif type == 'multiple':
        template_rating = template.choice_rating
    else:
        template_rating = template.rating

    expected_user = (1+10**((template_rating-user_rating)/400))**(-1)
    expected_template = (1+10**((template_rating-user_rating)/400))**(-1)
    prefactor_user = 30  # This value should be adjusted according to elo of the user (lower for higher ratings..)
    prefactor_template = 16  # This value should be adjusted according to elo of the user (lower for higher ratings..)
    minimum_answered_questions = 20  # Amount of questions the user needs to have answered for template rating to change
    if user_won:
        new_user_rating = user_rating + prefactor_user*(1-expected_user)
        new_template_rating = template_rating + prefactor_template*(0-expected_template)
        template.times_solved += 1
    else:
        new_user_rating = user_rating + prefactor_user*(0-expected_user)
        new_template_rating = template_rating + prefactor_template*(1-expected_template)
        template.times_failed += 1
    user_progress.level_rating = new_user_rating
    user_progress.questions_answered += 1
    user_progress.save()
    if user_progress.questions_answered <= minimum_answered_questions:
        new_template_rating = template_rating
    if type == 'blanks':
        template.fill_rating = new_template_rating
    elif type == 'multiple':
        template.choice_rating = new_template_rating
    else:
        template.rating = new_template_rating
    template.save()
    new_star = check_for_new_star(user, level_id)
    return (user_progress.level_rating, new_star)


def get_user_rating(user):
    """Returns the rating of the give user"""
    u = User.objects.get(username=user.username)
    rating = u.extendeduser.rating
    return rating


def check_for_new_star(user, level_id):
    """Checks if the user has earned a new star on a level"""
    new_star = False
    u = User.objects.get(username=user.username)
    level = Level.objects.get(pk=level_id)
    user_progress = UserLevelProgress.objects.get(user=u, level=level)
    rating = user_progress.level_rating
    stars = user_progress.stars
    r = [1600, 1800, 2000]
    if (rating > r[0] and stars == 0) or (rating > r[1] and stars == 1) or (rating > r[2] and stars == 2):
        add_star(user_progress)
        new_star = True
    return new_star


def add_star(user_progress):
    """Adds a star to a given user progress."""
    user_progress.stars += 1
    user_progress.save()


def calculate_offset(template, rating_change):
    """Calculates the offset that is used for rating balance"""
    difficulty = template.difficulty
    templates = Template.objects.all().filter(difficulty=1)
    num_templates = templates.count()
    offset = get_offset(difficulty)
    offset.offset += rating_change/num_templates
    offset.save()


def get_offset(difficulty):
    """Gets the offset for given difficulty, or creates one if none exist for that difficulty."""
    try:
        offset = Offset.objects.get(difficulty_number=difficulty)
    except Offset.DoesNotExist:
        offset = Offset(difficulty_number=difficulty)
        offset.save()
    return offset