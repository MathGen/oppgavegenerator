from random import randint

from oppgavegen.models import Template, UserLevelProgress, User
from oppgavegen.utility.decorators import Debugger


@Debugger
def get_question(user, template_id, topic=''):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 60
    increase = 15
    q = ''
    template_type = 'normal'
    if template_id == '':
        u = User.objects.get(username=user.username)
        user_rating = u.extendeduser.rating
        while True:
            q = Template.objects.filter(rating__gt=(user_rating-slack))
            q = q.filter(rating__lt=(user_rating+slack))
            q = q.filter(valid_flag=True)

            m = Template.objects.filter(choice_rating__gt=(user_rating-slack))
            m = m.filter(choice_rating__lt=(user_rating+slack))
            m = m.filter(valid_flag=True)
            m = m.filter(multiple_support=True)

            f = Template.objects.filter(fill_rating__gt=(user_rating-slack))
            f = f.filter(fill_rating__lt=(user_rating+slack))
            f = f.filter(valid_flag=True)
            f = f.filter(fill_in_support=True)

            # Use count instead of len as len loads the records.
            # Using len would be faster if we had to load all the records to python objects.
            length_normal = q.count()
            length_multiple = m.count()
            length_fill_in = f.count()
            length_total = length_fill_in + length_normal + length_multiple
            if length_total > 0:
                r_number = randint(1, length_total)
                if r_number <= length_fill_in and length_fill_in > 0:
                    q = f[r_number - 1]
                    template_type = 'blanks'
                elif r_number <= length_multiple + length_fill_in and length_multiple > 0:
                    template_type = 'multiple'
                    q = m[r_number - length_fill_in - 1]
                else:
                    q = q[r_number - length_fill_in - length_multiple - 1]
                break
            slack += increase

            if slack >= 800:
                q = Template.objects.all()
                q = q.latest('id')
                break
    else:
        q = Template.objects.get(pk=template_id)

    # test
    #b = Level.objects.all()
    #print(b)
    #print(b.filter(template__topic__topic__contains='Integrasjon'))
    return {'template': q, 'type': template_type}


@Debugger
def get_level_question(user, level):
    """Gets a template from the database at a appropriate rating.

    :param user: The user requesting a template
    :param template_id: (optional) the id of a template
    :param topic: the topic of the template.
    :return: Template object.
    """
    slack = 100
    increase = 15
    user_progress = add_level_to_user(user, level)
    offset = level.offset
    user_rating = user_progress.level_rating + offset
    while True:
        q = level.templates.all()
        q = q.filter(rating__gt=(user_rating-slack))
        q = q.filter(rating__lt=(user_rating+slack))
        q = q.filter(valid_flag=True)

        m = level.templates.all()
        m = m.filter(choice_rating__gt=(user_rating-slack))
        m = m.filter(choice_rating__lt=(user_rating+slack))
        m = m.filter(valid_flag=True)
        m = m.filter(multiple_support=True)

        f = level.templates.all()
        f = f.filter(fill_rating__gt=(user_rating-slack))
        f = f.filter(fill_rating__lt=(user_rating+slack))
        f = f.filter(valid_flag=True)
        f = f.filter(fill_in_support=True)

        # Use count instead of len as len loads the records.
        # Using len would be faster if we had to load all the records to python objects.
        length_normal = q.count()
        length_multiple = m.count()
        length_fill_in = f.count()
        length_total = length_fill_in + length_normal + length_multiple
        if length_total > 0:
            r_number = randint(1, length_total)
            if r_number <= length_fill_in and length_fill_in > 0:
                q = f[r_number - 1]
                template_type = 'blanks'
            elif r_number <= length_multiple + length_fill_in and length_multiple > 0:
                template_type = 'multiple'
                q = m[r_number - length_fill_in - 1]
            else:
                template_type = 'normal'
                q = q[r_number - length_fill_in - length_multiple - 1]
            break
        slack += increase

        if slack >= 1200:
            q = level.templates.all().order_by('?').first()
            template_type = 'normal'
            break
    return {'template': q, 'type': template_type}


@Debugger
def add_level_to_user(user, level):
    try:
        user_progress = UserLevelProgress.objects.get(user=user, level=level)
    except UserLevelProgress.DoesNotExist:
        user_progress = UserLevelProgress()
        user_progress.user = user
        user_progress.level = level
        user_progress.questions_answered = 0
        user_progress.save()
    return user_progress