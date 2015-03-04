from django import template
from django.contrib.auth.models import Group
register = template.Library()


def is_teacher(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()
