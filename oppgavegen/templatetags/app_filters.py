from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from oppgavegen.models import ExtendedUser, Set, Chapter, Level, Template
from django.core.paginator import Paginator
register = template.Library()


@register.filter
def is_teacher(user):
    """Returns True/False depending on if the user is a teacher"""
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()


@register.filter
def is_superuser(user):
    """Returns True/False depending on if the user is a superuser"""
    if user.is_superuser:
        return True
    return False


@register.filter
def get_rating(user):
    """Returns the users rating"""
    try:
        u = User.objects.get(username=user.username)
        rating = u.extendeduser.rating
    except ExtendedUser.DoesNotExist:
        rating = ''

    return rating


@register.filter
def get_current_set(user):
    try:
        set = user.extendeduser.current_set
    except ExtendedUser.DoesNotExist:
        set = ''
    return set


@register.filter
def get_current_chapter(user):
    try:
        chapter = user.extendeduser.current_chapter
    except ExtendedUser.DoesNotExist:
        chapter = ''
    return chapter


@register.filter
def get_current_level(user):
    try:
        level = user.extendeduser.current_level
    except ExtendedUser.DoesNotExist:
        level = ''
    return level


@register.filter
def user_in_set(user, set_id):
    """Returns true/false depending on if the user is in the set"""
    set = Set.objects.get(pk=set_id)
    user_in_set = set.users.all().filter(id=user.id).exists()
    return user_in_set


@register.inclusion_tag('includes/user_templates.html')
def get_user_templates(user):
    templates = Template.objects.all().filter(editor=user,copy=False)
    return {'templates':templates}

@register.inclusion_tag('includes/user_sets.html')
def get_user_objects(user, object_type):
    types = ['set','chapter','level']
    objects = ""
    if object_type == 'set':
        objects = Set.objects.all().filter(editor=user,copy=False)
    elif object_type == 'chapter':
        objects = Chapter.objects.all().filter(editor=user,copy=False)
    elif object_type == 'level':
        objects = Level.objects.all().filter(creator=user,copy=False)
    else:
        objects = Set.objects.none()
    return {'objects': objects, 'type': object_type, 'types': types}