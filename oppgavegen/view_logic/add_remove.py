from django.http import HttpResponse
from oppgavegen.models import Level, Template, Set, Chapter
from datetime import datetime
from oppgavegen.models import ExtendedUser


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


def remove_chapter(chapter_id, user):
    chapter = Chapter.objects.get(pk=chapter_id)
    success_string = 'Failed to delete chapter ' + chapter.name + '.'
    if chapter.editor == user:
        success_string = 'Chapter sucessfully deleted' + chapter.name + '.'
        reset_current_chapter(user)
        chapter.delete()
    return success_string


def remove_level(level_id, user):
    level = Level.objects.get(pk=level_id)
    success_string = 'Failed to delete chapter ' + level.name + '.'
    if level.editor == user:
        success_string = 'Chapter sucessfully deleted' + level.name + '.'
        reset_current_level(user)
        level.delete()
    return success_string


def remove_set(set_id, user):
    set = Set.objects.get(pk=set_id)
    success_string = 'failed to delete set: "' + set.name + '".'
    if set.editor == user:
        success_string = 'set sucessfully deleted: "' + set.name + '".'
        reset_current_set(user)
        set.delete()
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
        level.chapters.remove(template)
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


def update_chapter_or_set(set_or_chapter, title, order, user):
    msg = 'Failed update.'
    if set_or_chapter.creator == user:
        set_or_chapter.name = title
        set_or_chapter.order = order
        set_or_chapter.save()

        msg = 'Successful update'
    return msg

def update_level(level, title, user, k_factor):
    msg = 'Failed update.'
    if level.creator == user:
        level.name = title
        level.k_factor = k_factor
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

def add_user_to_set(user, set_id):
    msg = 'success'
    try:
        set = Set.objects.get(pk=set_id)
        set.users.add(user)
        set.save()
    except Exception as e:
        print('exception in add_user_to_set')
        print(e)
        msg = 'failed to add user to set'
    return msg