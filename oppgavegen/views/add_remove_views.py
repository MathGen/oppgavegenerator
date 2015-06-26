"""For views that either add or remove something from the database"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from oppgavegen.models import Level, Template, Set, Chapter
from oppgavegen.view_logic.add_remove import *


def add_level_to_current_chapter(request, level_id):
    """Add a template to the current level a teacher user is working on."""
    chapter = request.user.extendeduser.current_chapter
    level = Template.objects.get(pk=level_id)
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
        chapter = new_chapter(chapter_name, request.user)
        add_chapter_to_set(chapter, set)
        print('end')

        return HttpResponse(chapter.pk)


def remove_chapter_from_set(request, set_id, chapter_id):
    """Deletes a chapter from a set"""
    msg = remove_from_set(set_id, chapter_id, request.user)
    remove_chapter(chapter_id, request.user)

    return HttpResponse(msg)