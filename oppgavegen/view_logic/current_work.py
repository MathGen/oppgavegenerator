

def set_current_set(user, set):
    if user.extendeduser.current_set != set:
        user.extendeduser.current_set = set
        user.extendeduser.current_chapter = None
        user.extendeduser.current_level = None
        user.extendeduser.save()
    pass

def set_current_chapter(user, chapter):
    if user.extendeduser.current_chapter != chapter:
        user.extendeduser.current_chapter = chapter
        user.extendeduser.current_level = None
        user.extendeduser.save()

def set_current_level(user, level):
    if user.extendeduser.current_level != level:
        user.extendeduser.current_level = level
        user.extendeduser.save()