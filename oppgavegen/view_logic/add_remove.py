from django.http import HttpResponse
from oppgavegen.models import Level, Template, Set, Chapter
from datetime import datetime
from oppgavegen.models import ExtendedUser, User
from copy import deepcopy


def new_chapter(chapter_name, user):
    chapter = Chapter(name=chapter_name, editor=user, creator=user, creation_date=datetime.now(), copy=False)
    chapter.save()
    return chapter


def new_level(level_name, user):
    level = Level(name=level_name, creator=user, editor=user, creation_date=datetime.now(), k_factor=3, copy=False)
    level.save()
    return level


def new_set(set_name, user):
    set = Set(name=set_name, creator=user, editor=user, creation_date=datetime.now(), copy=False)
    set.save()
    return set

def remove_level(level_id, user):
    level = Level.objects.get(pk=level_id)
    success_string = 'Failed to delete chapter ' + level.name + '.'
    if level.editor == user:
        success_string = 'Chapter sucessfully deleted' + level.name + '.'
        reset_current_level(user)
        level.delete()
    return success_string


def remove_chapter(chapter_id, user):
    chapter = Chapter.objects.get(pk=chapter_id)
    success_string = 'Failed to delete chapter ' + chapter.name + '.'
    if chapter.editor == user:
        success_string = 'Chapter sucessfully deleted' + chapter.name + '.'
        reset_current_chapter(user)
        chapter.delete()
    return success_string


def remove_set(set_id, user):
    set = Set.objects.get(pk=set_id)
    success_string = 'failed to delete set: "' + set.name + '".'
    if set.editor == user:
        success_string = 'set sucessfully deleted: "' + set.name + '".'
        reset_current_set(user)
        set.delete()
    return success_string

def delete_set_and_related_copies(set_id,user):
    set = Set.objects.get(pk=set_id)
    chapters_to_delete = []
    c_count = 0
    levels_to_delete = []
    l_count = 0
    templates_to_delete = []
    t_count = 0
    success_string = "Set deletion failed."
    if set.editor == user:
        chapter_ids = set.order
        if len(chapter_ids) > 0:
            for c_id in chapter_ids.split(','):
                chapter = Chapter.objects.get(pk=int(c_id))
                if chapter.copy == True:
                    chapters_to_delete.append(chapter)
                level_ids = chapter.order
                if len(level_ids) > 0:
                    for l_id in level_ids.split(','):
                        level = Level.objects.get(pk=int(l_id))
                        if level.copy == True:
                            levels_to_delete.append(level)
                        template_ids = level.templates.values_list('id',flat=True)
                        if len(template_ids) > 0:
                            for t_id in template_ids:
                                template = Template.objects.get(pk=int(t_id))
                                if template.copy == True:
                                    templates_to_delete.append(template)

        for t in templates_to_delete:
            t_count+=1
            t.delete()
        for l in levels_to_delete:
            l_count+=1
            l.delete()
        for c in chapters_to_delete:
            c_count+=1
            c.delete()
        reset_current_set(user)
        set.delete()
        success_string = 'successfully deleted set ' + set.name + ', ' \
                     + str(t_count) + ' templates, ' \
                     + str(l_count) + ' levels, and ' \
                     + str(c_count) + ' chapters.'
    return success_string

def delete_chapter_and_related_copies(chapter_id,user):
    chapter = Chapter.objects.get(pk=chapter_id)
    levels_to_delete = []
    l_count = 0
    templates_to_delete = []
    t_count = 0
    success_string = "Chapter deletion failed."
    if chapter.editor == user:
        level_ids = chapter.order
        if len(level_ids) > 0:
            for l_id in level_ids.split(','):
                level = Level.objects.get(pk=int(l_id))
                if level.copy == True:
                    levels_to_delete.append(level)
                template_ids = level.templates.values_list('id',flat=True)
                if len(template_ids) > 0:
                    for t_id in template_ids:
                        template = Template.objects.get(pk=int(t_id))
                        if template.copy == True:
                            templates_to_delete.append(template)

        for t in templates_to_delete:
            t_count+=1
            t.delete()
        for l in levels_to_delete:
            l_count+=1
            l.delete()
        reset_current_chapter(user)
        chapter.delete()
        success_string = 'successfully deleted chapter ' + chapter.name + ', ' \
                     + str(t_count) + ' templates, and ' \
                     + str(l_count) + ' levels.'
    return success_string

def delete_level_and_related_copies(level_id,user):
    level = Level.objects.get(pk=level_id)
    templates_to_delete = []
    t_count = 0
    success_string = "Level deletion failed."
    if level.editor == user:
        template_ids = level.templates.values_list('id',flat=True)
        if len(template_ids) > 0:
            for t_id in template_ids:
                template = Template.objects.get(pk=int(t_id))
                if template.copy == True:
                    templates_to_delete.append(template)

        for t in templates_to_delete:
            t_count+=1
            t.delete()
        reset_current_level(user)
        level.delete()
        success_string = 'successfully deleted level ' + level.name + ', and ' \
                         + str(t_count) + ' templates.'
    return success_string


def remove_chapter_from_set(set_id, chapter_id, user):
    set = Set.objects.get(pk=set_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    success_message = 'Failed to remove ' + chapter.name + ' from set.'
    if user == set.editor:
        set.chapters.remove(chapter)
        order = set.order.split(',')
        order.remove(chapter_id)
        order = ','.join(order)
        set.order = order
        set.save()
        success_message = 'successfully removed ' + chapter.name + ' from set.'

    return success_message


def remove_level_from_chapter(chapter_id, level_id, user):
    chapter = Chapter.objects.get(pk=chapter_id)
    level = Level.objects.get(pk=level_id)
    success_message = 'Failed to remove ' + level.name + ' from set.'
    if user == chapter.editor:
        chapter.levels.remove(level)
        order = chapter.order.split(',')
        order.remove(level_id)
        order = ','.join(order)
        chapter.order = order
        chapter.save()
        success_message = 'successfully removed ' + level.name + ' from set.'

    return success_message


def remove_template_from_level(level_id, template_id, user):
    level = Level.objects.get(pk=level_id)
    template = Template.objects.get(pk=template_id)
    success_message = 'Failed to remove ' + template.name + ' from set.'
    if user == level.editor:
        level.templates.remove(template)
        level.save()
        success_message = 'successfully removed ' + template.name + ' from set.'

    return success_message


def add_template_to_level(template, level, user):
    success_message = 'Failed to add template to level'
    if level.editor == user:
        level.templates.add(template)
        level.save()
        success_message = 'successfully added template to level'
    return success_message


def remove_template(template_id, user):
    template = Template.objects.get(pk=template_id)
    success_string = 'Failed to delete template ' + template.name + '.'
    if template.editor == user:
        success_string = 'Successfully deleted template' + template.name + '.'
        template.delete()
    return success_string


def add_level_to_chapter(level, chapter):
    add_to_level_order = ''
    if chapter.order != '':
        add_to_level_order = ','
    chapter.order += add_to_level_order + str(level.pk)
    chapter.levels.add(level)
    chapter.save()


def add_chapter_to_set(chapter, set):
    add_to_level_order = ''
    if set.order != '':
        add_to_level_order = ','
    if set.is_requirement:
        chapter.in_requirement_set = True
        chapter.save()
    set.order += add_to_level_order + str(chapter.pk)
    set.chapters.add(chapter)
    set.save()


def make_copy(original, user):
    copy = original
    copy.pk = None
    copy.editor = user
    copy.copy = True
    copy.save()
    return copy


def make_set_copy(original_set, user, copy_as_requirement=False):
    set_copy = original_set
    set_copy.pk = None
    set_copy.editor = user
    set_copy.copy = True
    set_copy.is_public = False
    if copy_as_requirement == True:
        set_copy.is_requirement = True
    set_copy.save()
    chapter_ids = set_copy.order
    set_copy.order = ""
    if len(chapter_ids) > 0:
        for c_id in chapter_ids.split(','): # get chapters id's from set order list
            chapter = Chapter.objects.get(pk=int(c_id))
            c_copy = make_copy(chapter,user)
            level_ids = c_copy.order
            c_copy.order = ""
            if copy_as_requirement: # this is the only case where this should be set to true
                c_copy.in_requirement_set = True
            c_copy.save()
            add_chapter_to_set(c_copy,set_copy)
            if len(level_ids) > 0:
                for l_id in level_ids.split(','):
                    level = Level.objects.get(pk=int(l_id))
                    templates = level.templates.all()
                    template_ids = templates.values_list('id', flat=True)
                    l_copy = make_copy(level,user)
                    add_level_to_chapter(l_copy,c_copy)
                    if len(template_ids) > 0:
                        for t_id in template_ids:
                            template = Template.objects.get(pk=int(t_id))
                            t_copy = make_copy(template,user)
                            add_template_to_level(t_copy,l_copy,user)
    return set_copy

def make_chapter_copy(original_chapter, user):
    c_copy = original_chapter
    c_copy.pk = None
    c_copy.copy = True
    c_copy.editor = user
    level_ids = c_copy.order
    c_copy.order = ""
    c_copy.save()
    if len(level_ids) > 0:
        for l_id in level_ids.split(','):
            level = Level.objects.get(pk=int(l_id))
            templates = level.templates.all()
            template_ids = templates.values_list('id', flat=True)
            l_copy = make_copy(level,user)
            add_level_to_chapter(l_copy,c_copy)
            if len(template_ids) > 0:
                for t_id in template_ids:
                    template = Template.objects.get(pk=int(t_id))
                    t_copy = make_copy(template,user)
                    add_template_to_level(t_copy,l_copy,user)
    return c_copy

def make_level_copy(original_level, user):
    l_copy = original_level
    l_copy.copy = True
    l_copy.editor = user
    templates = original_level.templates.all()
    template_ids = templates.values_list('id', flat=True)
    l_copy.pk = None
    l_copy.save()
    if len(template_ids) > 0:
        for t_id in template_ids:
            template = Template.objects.get(pk=int(t_id))
            t_copy = make_copy(template,user)
            add_template_to_level(t_copy,l_copy,user)
    return l_copy


def update_set(set, title, order, password, user):
    msg = 'Failed update.'
    if set.editor == user:
        set.name = title
        set.order = order
        if len(password) > 0:
            set.password = password
            set.password_protected = True
        else:
            set.password_protected = False
        set.save()

        msg = 'Successful update'
    return msg


def update_chapter(set_or_chapter, title, order, user):
    msg = 'Failed update.'
    if set_or_chapter.editor == user:
        set_or_chapter.name = title
        set_or_chapter.order = order
        set_or_chapter.save()

        msg = 'Successful update'
    return msg


def update_level(level, title, user, k_factor, k_factor_template, randomness):
    msg = 'Failed update.'
    if level.editor == user:
        level.name = title
        level.k_factor = k_factor
        level.k_factor_template = k_factor_template
        level.randomness = randomness
        level.save()
        msg = 'Successful update'
    return msg

def reset_current_set(user):
    euser = ExtendedUser.objects.get(user=user)
    euser.current_set = None
    euser.current_chapter = None
    euser.current_level = None
    euser.save()

def reset_current_chapter(user):
    euser = ExtendedUser.objects.get(user=user)
    euser.current_chapter = None
    euser.current_level = None
    euser.save()

def reset_current_level(user):
    euser = ExtendedUser.objects.get(user=user)
    euser.current_level = None
    euser.save()

def add_user_to_set(user, user_password, set_id):
    msg = 'success'
    try:
        set = Set.objects.get(pk=set_id)
        if set.password_protected:
            if set.password != user_password:
                msg = 'bad password'
            else:
                set.users.add(user)
                set.save()
        else:
            set.users.add(user)
            set.save()
    except Exception as e:
        print('exception in add_user_to_set')
        print(e)
        msg = 'failed to add user to set'
    return msg

def remove_user_from_set(user_id, set_id):
    # remove a user from a set and all level progression tables from related levels in related chapters
    # to clean up statistics views
    msg = 'success'
    user = User.objects.get(pk=user_id)
    # get the set and prefetch related chapters, levels and student level progress-entries
    try:
        set = Set.objects.filter(id__exact=set_id).prefetch_related('chapters','chapters__levels',
                                                                    'chapters__levels__student_progresses')

        chapters = set[0].chapters.all()
        level_lists = []
        progress_entry_lists = []  # lists of progress entries to delete

        for chapter in chapters:
            level_lists.append(chapter.levels.all())  # add lists of levels to level list
            for level_list in level_lists:
                for level in level_list:
                    progress_entry_lists.append(level.student_progresses.filter(user__id=user_id))

        for entry_list in progress_entry_lists:
            for entry in entry_list:
                entry.delete()  # delete level progress entries

        user.sets_joined.remove(set[0])  # remove the user/set relation
        user.save()


    except Exception as e:
        print('exception in remove_user_from_set')
        print(e)
        msg = 'failed to remove user from set'
    return msg
