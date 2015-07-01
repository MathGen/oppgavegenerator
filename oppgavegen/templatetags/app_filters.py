from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
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
    u = User.objects.get(username=user.username)
    rating = u.extendeduser.rating
    return rating