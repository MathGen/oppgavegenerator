from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from oppgavegen.models import ExtendedUser
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