from oppgavegen.models import ExtendedUser
from django.contrib.auth.models import User

def set_current_set(user, set):
    if user.ExtendedUser.current_set != set:
        user.ExtendedUser.current_set = set
        user.ExtendedUser.current_chapter = None
        user.ExtendedUser.current_level = None
        user.ExtendedUser.save()
    pass

def set_current_chapter(user, chapter):
    if user.ExtendedUser.current_chapter != chapter:
        user.ExtendedUser.current_chapter = chapter
        user.ExtendedUser.current_level = None
        user.ExtendedUser.save()

def set_current_level(user, level):
    if user.ExtendedUser.current_level != level:
        user.ExtendedUser.current_level = level
        user.ExtendedUser.save()