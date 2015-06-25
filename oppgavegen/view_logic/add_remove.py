from django.http import HttpResponse
from oppgavegen.models import Level, Template, Set, Chapter

def new_chapter(chapter_name, user):
    print('new chapter: 1')
    chapter = Chapter(name=chapter_name, creator=user)  # todo: add data time now pls
    print('new chapter: 2')
    chapter.save()
    return chapter


def new_level(level_name, user):
    level = Level(name=level_name, user=user)
    level.save()
    return level


def new_set(set_name, user):
    set = Set(name=set_name, user=user)
    set.save()
    return set


def add_template_to_level(template, level):
    level.levels.add(template)
    level.save()


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