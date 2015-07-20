"""Functions related to rating change."""

from oppgavegen.models import User, UserLevelProgress, Level, Template
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
    k_factor = level.k_factor
    if k_factor < 3:
        k_factor = k_factor/4
    else:
        k_factor -= 2
    offset = level.offset
    # Formula for elo: Rx = Rx(old) + prefactor *(W-Ex) where W=1 if wins and W=0 if x loses
    # and Ex is the expected probability that x will win.
    # Ea = (1+10^((Rb-Ra)/400))^-1
    # Eb = (1+10^((Ra-Rb)/400))^-1
    if type == 'blanks':
        template_rating = template.fill_rating
        difficulty = template.difficulty_blanks
    elif type == 'multiple':
        template_rating = template.choice_rating
        difficulty = template.difficulty_multiple
    else:
        template_rating = template.rating
        difficulty = template.difficulty

    expected_user = (1+10**((template_rating-user_rating+offset)/400))**(-1)
    expected_template = (1+10**((template_rating-user_rating+offset)/400))**(-1)
    prefactor_user = 30  # This value should be adjusted according to elo of the user (lower for higher ratings..)
    prefactor_template = 16  # This value should be adjusted according to elo of the user (lower for higher ratings..)
    minimum_answered_questions = 20  # Amount of questions the user needs to have answered for template rating to change

    if user_won:
        new_user_rating = user_rating + prefactor_user*(1-expected_user)*k_factor
        new_template_rating = template_rating + prefactor_template*(0-expected_template)
        template.times_solved += 1
    else:
        new_user_rating = user_rating + prefactor_user*(0-expected_user)*k_factor
        new_template_rating = template_rating + prefactor_template*(1-expected_template)
        template.times_failed += 1

    new_user_rating = round(new_user_rating)
    user_progress.level_rating = max(new_user_rating, 1)
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

    template_rating_change = new_template_rating - template_rating  # How much the templates rating has changed
    calculate_and_save_offset(template_rating_change, level, difficulty)

    new_star = check_for_new_star(user, level_id)
    return (user_progress.level_rating, new_star)


def get_user_rating(user):
    """Returns the rating of the given user"""
    u = User.objects.get(username=user.username)
    rating = u.extendeduser.rating
    return rating

def check_for_new_star(user, level_id):
    """Checks if the user has earned a new star on a level"""
    new_star = 0
    u = User.objects.get(username=user.username)
    level = Level.objects.get(pk=level_id)
    user_progress = UserLevelProgress.objects.get(user=u, level=level)
    rating = user_progress.level_rating
    stars = user_progress.stars
    r = [1300, 1450, 1600, 1800, 2000]
    if (rating > r[0] and stars == 0) or (rating > r[1] and stars == 1) or (rating > r[2] and stars == 2)\
            or (rating > r[3] and stars == 3) or (rating > r[3] and stars == 3):
        add_star(user_progress)
        new_star = 1
    return new_star


def add_star(user_progress):
    """Adds a star to a given user progress."""
    user_progress.stars += 1
    user_progress.save()


def calculate_and_save_offset(rating_change, level, difficulty):
    """Calculates the offset that is used for rating balance and saves it"""
    upper = 15  # The upper bound of templates used for offset
    lower = 11  # The lower bound of templates used for offset

    if difficulty < upper and difficulty > lower:
        num_templates = Template.objects.all().filter(difficulty__gt=lower, difficulty__lt=upper).count()
        num_templates += Template.objects.all().filter(difficulty_multiple__gt=lower, difficulty_multiple__lt=upper).count()
        num_templates += Template.objects.all().filter(difficulty_blanks__gt=lower, difficulty_blanks__lt=upper).count()

        level.offset += rating_change/num_templates
        level.save()


