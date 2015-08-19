"""For views that either add or remove something from the database"""
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from oppgavegen.models import Level, Template, Set, Chapter
from oppgavegen.view_logic.add_remove import *
import json
from django.utils.encoding import force_text

def new_set_view(request, set_name='Navn på sett'):
    """View for creating a new set"""
    user = request.user
    set = new_set(set_name, user)

    return HttpResponse(set.pk)

def remove_set_view(request, set_id):
    """View for deleting a set"""
    user = request.user
    msg = delete_set_and_related_copies(set_id,user)

    return HttpResponse(msg)

def add_level_to_current_chapter_view(request, level_id):
    """Add a template to the current level a teacher user is working on."""
    chapter = request.user.extendeduser.current_chapter
    level = Level.objects.get(pk=level_id)
    if level.editor == request.user:
        add_level_to_chapter(level, chapter)
        return HttpResponse('Level lagt til Chapter "'
                            + chapter.name +
                            '".')
    else:
        return HttpResponse('Du må være eier av kapitellet for å legge til level')


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


def remove_template_from_level_view(request, level_id, template_id):
    msg = remove_template_from_level(level_id, template_id, request.user)
    remove_template(template_id,request.user)
    return HttpResponse(msg)


def remove_chapter_from_set_view(request, set_id, chapter_id):
    """Deletes a chapter from a set"""
    remove_chapter_from_set(set_id, chapter_id, request.user)
    msg = delete_chapter_and_related_copies(chapter_id, request.user)

    return HttpResponse(msg)


def remove_level_from_chapter_view(request, chapter_id, level_id):
    """Deletes a chapter from a set"""
    remove_level_from_chapter(chapter_id, level_id, request.user)
    msg = delete_level_and_related_copies(level_id, request.user)
    return HttpResponse(msg)

def add_template_to_level_view(request, level_id, template_id):
    msg = 'Failed to add template to level.'
    level = Level.objects.get(pk=level_id)
    template = Template.objects.get(pk=template_id)
    user = request.user
    if level.editor == user:
        template = make_copy(template, user)
        add_template_to_level(template, level, request.user)
        msg = {'id': template.id, 'name': template.name}
        msg = json.dumps(msg)

    return HttpResponse(msg)


def add_level_to_chapter_view(request, chapter_id, level_id):
    """Add a level fo a specified chapter"""
    msg = 'Failed to add level to chapter'
    if request.is_ajax():
        chapter = Chapter.objects.get(pk=chapter_id)
        user = request.user
        level = Level.objects.get(pk=level_id)
        if chapter.editor == user:
            level = make_level_copy(level, user)
            add_level_to_chapter(level, chapter)
            msg = {'id': level.id, 'name': level.name}
            msg = json.dumps(msg)

    return HttpResponse(msg)


def add_chapter_to_set_view(request, set_id, chapter_id):
    """Add a chapter fo a specified set"""
    msg = 'Failed to add chapter to set'
    try:
        if request.is_ajax():
            set = Set.objects.get(pk=set_id)
            user = request.user
            chapter = Chapter.objects.get(pk=chapter_id)
            if set.editor == user:
                chapter = make_chapter_copy(chapter, user)
                add_chapter_to_set(chapter, set)
                msg = {'id': chapter.id, 'name': chapter.name}
                msg = json.dumps(msg)
    except Exception as e:
        print(e)

    return HttpResponse(msg)

def add_set_to_user_view(request, set_id):
    """Makes a copy of a set and adds it to a user's collection"""
    msg = 'Failed to copy set'
    try:
        if request.is_ajax():
            set = Set.objects.get(pk=set_id)
            user = request.user
            new_set = make_set_copy(set, user)
            msg = {'id': new_set.id, 'name': new_set.name}
            msg = json.dumps(msg)
    except Exception as e:
        print(e)

    return HttpResponse(msg)

def copy_set_as_requirement(request,set_id):
    """ Copy a set and mark it as a requirement """
    msg = 'Failed to create requirement from set'
    try:
        if request.is_ajax():
            set = Set.objects.get(pk=set_id)
            user = request.user
            req_set = make_set_copy(original_set=set, user=user, copy_as_requirement=True)
            msg = {'id': req_set.id, 'name': req_set.name}
            msg = json.dumps(msg)
    except Exception as e:
        print(e)

    return HttpResponse(msg)

def update_chapter_view(request):
    msg = 'Noe gikk galt'
    if request.method == 'POST':
        form = request.POST
        title = form['title']
        order = form['order']
        chapter_id = int(form['chapter_id'])
        chapter = Chapter.objects.get(pk=chapter_id)
        msg = update_chapter_or_set(chapter, title, order, request.user)
    return HttpResponse(msg)

def update_set_view(request):
    msg = 'Noe gikk galt'
    if request.method == 'POST':
        form = request.POST
        title = form['title']
        order = form['order']
        set_id = int(form['set_id'])
        set = Set.objects.get(pk=set_id)
        msg = update_chapter_or_set(set, title, order, request.user)

    return HttpResponse(msg)

def update_object_name(request, object):
    "Set an object name"
    if object.editor == request.user:
        if request.method == 'POST':
            form = request.post
            title = form['title']
            object.update(name=title)

    return HttpResponse(object.title)

def update_level_view(request):
    msg = 'Noe gikk galt'
    if request.method == 'POST':
        form = request.POST
        title = form['title']
        k_factor = form['k_factor']
        level_id = int(form['level_id'])
        level = Level.objects.get(pk=level_id)
        msg = update_level(level, title, request.user, k_factor)
    return HttpResponse(msg)

def add_user_to_set_view(request):
    print("it's a start")
    try:
        msg = 'noe gikk galt'
        if request.method == 'POST':
            form = request.POST
            set_id = int(form['set_id'])
            msg = add_user_to_set(request.user, set_id)
    except Exception as e:
        print('error')
        print(e)
    return HttpResponse(msg)

def toggle_template_level_membership(request, template_id):
    """"
    Toggle template->level membership via ajax POST without making a copy.
    For Advanced Search-results where the user is the editor (owner).
    """
    msg = ''
    level = request.user.extendeduser.current_level
    if request.method == 'POST':
        try:
            template = Template.objects.get(pk=template_id)
        except Template.DoesNotExist as e:
            raise ValueError("Unknown template.id=" + str(template_id) + "or level.id=" +
                             str(level.id) + ". Original error: " + str(e))
        if template in level.templates.all():
            level.templates.remove(template)
            level.save()
            msg = "Template " + str(template.id) + " removed from " + level.name
        else:
            level.templates.add(template)
            msg = "Template " + str(template.id) + " added to " + level.name
    return HttpResponse(msg)