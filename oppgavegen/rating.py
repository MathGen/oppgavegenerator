from oppgavegen.models import User, UserLevelProgress, Level
from oppgavegen.decorators import Debugger

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
    prefactor_user = 30  # This value should be adjusted according to elo of the user (lower for higher ratings..)
    prefactor_template = 16  # This value should be adjusted according to elo of the user (lower for higher ratings..)

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

    if user_won:
        new_user_rating = user_rating + prefactor_user*(1-expected_user)
        new_template_rating = template_rating + prefactor_template*(0-expected_template)
        template.times_solved += 1
    else:
        new_user_rating = user_rating + prefactor_user*(0-expected_user)
        new_template_rating = template_rating + prefactor_template*(1-expected_template)
        template.times_failed += 1
    user_progress.level_rating = new_user_rating
    user_progress.save()

    if type == 'blanks':
        template.fill_rating = new_template_rating
    elif type == 'multiple':
        template.choice_rating = new_template_rating
    else:
        template.rating = new_template_rating
    template.save()
    check_for_new_star(user, level_id)
    return

def get_user_rating(user):
    """Returns the rating of the give user"""
    u = User.objects.get(username=user.username)
    rating = u.extendeduser.rating
    return rating


def check_for_new_star(user, level_id):
    u = User.objects.get(username=user.username)
    level = Level.objects.get(pk=level_id)
    user_progress = UserLevelProgress.objects.get(user=u, level=level)
    rating = user_progress.level_rating
    stars = user_progress.stars
    r = [1500, 1800, 2100]
    if (rating > r[0] and stars == 0) or (rating > r[1] and stars == 1) or (rating > r[2] and stars == 2):
        add_star(user_progress)
    pass


def add_star(user_progress):
    user_progress.stars += 1
    user_progress.save()


def calculate_offset():
    """Calculates the offset that is used for rating balance"""
    pass
