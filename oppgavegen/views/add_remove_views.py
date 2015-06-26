"""For views that either add or remove something from the database"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from oppgavegen.models import Level, Template, Set, Chapter
from oppgavegen.view_logic.add_remove import *


def add_level_to_current_chapter_view(request, level_id):
    """Add a template to the current level a teacher user is working on."""
    chapter = request.user.extendeduser.current_chapter
    level = Level.objects.get(pk=level_id)
    if level.creator == request.user:
        add_level_to_chapter(level, chapter)
        return HttpResponse('Template added to level "'
                            + level.name +
                            '". (This will be a background process eventually.)')
    else:
        return HttpResponse('Du må være eier a kapitellet for å legge til level')


def new_chapter_for_set(request, set_id, chapter_name):
    """Add a template fo a specified level"""
    if request.is_ajax():
        set = Set.objects.get(pk=set_id)
        msg = 'Failed to add chapter'
        if set.creator == request.user:
            chapter = new_chapter(chapter_name, request.user)
            add_chapter_to_set(chapter, set)
            msg = chapter.pk

        return HttpResponse(msg)


def new_level_for_chapter(request, chapter_id, level_name):
    """Add a template fo a specified level"""
    if request.is_ajax():

        chapter = Chapter.objects.get(pk=chapter_id)
        msg = 'Failed to add chapter'
        if chapter.creator == request.user:
            level = new_level(level_name, request.user)
            add_level_to_chapter(level, chapter)
            msg = level.pk
        return HttpResponse(msg)


def add_template_to_level_view(request, level_id, template_id):
    level = Level.objects.get(pk=level_id)
    template = Template.objects.get(pk=template_id)
    msg = add_template_to_level(template, level, request.user)

    return HttpResponse(msg)


def remove_template_from_level_view(request, level_id, template_id):
    msg = remove_template_from_level(level_id, template_id, request.user)
    return HttpResponse(msg)


def remove_chapter_from_set_view(request, set_id, chapter_id):
    """Deletes a chapter from a set"""
    msg = remove_chapter_from_set(set_id, chapter_id, request.user)
    remove_chapter(chapter_id, request.user)

    return HttpResponse(msg)


def remove_level_from_chapter_view(request, chapter_id, level_id):
    """Deletes a chapter from a set"""
    try:
        msg = remove_level_from_chapter(chapter_id, level_id, request.user)   # Todo: only remove if original creator.
        remove_level(level_id, request.user)
    except Exception as e:
        print(e)
    return HttpResponse(msg)


def add_level_to_chapter_view(request, chapter_id, level_id):
    """Add a template fo a specified level"""
    if request.is_ajax():
        chapter = Chapter.objects.get(pk=chapter_id)
        msg = 'Failed to add chapter'
        user = request.user
        level = Level.objects.get(pk=level_id)
        if chapter.creator == user or chapter.editor == user.name:
            level = make_copy(level, user)
            add_level_to_chapter(level, chapter)
            msg = level.pk

        return HttpResponse(msg)


def add_chapter_to_set_view(request, set_id, chapter_id):
    """Add a template fo a specified level"""
    if request.is_ajax():
        set = Set.objects.get(pk=set_id)
        msg = 'Failed to add chapter'
        user = request.user
        chapter = Chapter.objects.get(pk=chapter_id)
        if set.creator == user or set.editor == user.name:
            chapter = make_copy(chapter, user)
            add_level_to_chapter(chapter, set)
            msg = chapter.pk

        return HttpResponse(msg)