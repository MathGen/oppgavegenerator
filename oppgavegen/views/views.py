"""

Defines views, and renders data to html templates.

"""

import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from django.views.decorators.cache import cache_control

from oppgavegen.tables import *
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen.models import Set, Chapter, Level, Template
from oppgavegen.view_logic.rating import change_elo, change_level_rating, get_user_rating
from oppgavegen.generation_folder.generation import generate_task, generate_level
from oppgavegen.view_logic.progress import calculate_progress, chapter_progress, get_stars_per_level


# Search Views and Forms
from haystack.generic_views import SearchView
from oppgavegen.forms import QuestionForm, TemplateForm, LevelCreateForm, ChapterNameForm, UserCurrentSetsForm, SetsSearchForm
from django.forms.formsets import formset_factory
from django import http
from django.forms.models import inlineformset_factory



class LoginRequiredMixin(object):
    """ Generic @login_required Mixin for class-based views  """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def is_member(user):
    """Returns true/false depending on if the user is a member of the teacher group (or is a superuser)"""
    if user.is_superuser:
        return True
    return user.groups.filter(name='Teacher').exists()


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required
def task(request):
    """Returns a render of taskview.html with a rating apropriate math question"""
    context = RequestContext(request)
    question_type = request.GET.get('q', '')
    if question_type != "":
        context_dict = generate_task(request.user, question_type)
    else:
        context_dict = generate_task(request.user, "")
    context_dict['rating'] = get_user_rating(request.user)
    return render_to_response('taskview.html', context_dict, context)


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True) # Doesn't cache the page
@login_required
def task_by_id_and_type(request, template_extra, desired_type='normal'):
    """Returns a render of taskview with a specific math template with specified type"""
    context = RequestContext(request)
    context_dict = generate_task(request.user, template_extra, desired_type)
    context_dict['rating'] = get_user_rating(request.user)
    if context_dict['question'] == 'error':
        message = {'message': 'Denne oppgavetypen har ikke blitt laget for denne oppgaven'}
        return render_to_response('error.html', message, context)
    return render_to_response('taskview.html', context_dict, context)


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required
def task_by_extra(request, template_extra):
    """Returns a render of taskview with a specific math template"""
    context = RequestContext(request)
    context_dict = generate_task(request.user, template_extra)
    context_dict['rating'] = get_user_rating(request.user)
    return render_to_response('taskview.html', context_dict, context)


@login_required
@user_passes_test(is_teacher, '/')
def gen(request):
    """Returns a render of gen.html"""
    context = RequestContext(request)
    topics = ""
    for e in Topic.objects.all():  # Retrieves a list of topics and passes them to the view.
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics': topics}
    return render_to_response('gen.html', context_dict, context)


@login_required
@user_passes_test(is_teacher, '/')
def submit(request):
    """Returns a render of submit html. Different depending on if the submission goes through ot not"""
    message = 'don\'t come here'
    if request.method == 'POST':
        message = 'Det har skjedd noe feil ved innsending av form'
        form = TemplateForm(request.POST)
        if form.is_valid():
            newtags = form.cleaned_data['tags_list']
            template = form.save(commit=False)
            # newtags = template.tags_list
            # template.tags = newtags
            #template.fields['tags'] = form.cleaned_data['tags_list']
            #template.tags.add(templatetags)
            template.difficulty = 1 # todo: remove this when implemented in GUI. Default value doesn't work somehow.
            if request.REQUEST['pk'] != '':  # Can this be written as v = req != ''?
                template.pk = request.REQUEST['pk']  # Workaround, template doesn't automatically get template.pk
                update = True
            else:
                update = False
            message = submit_template(template, request.user, update, newtags)

        else:
            print(form.errors)
    context = RequestContext(request)
    return render_to_response('submit.html', {'message': message}, context)


@login_required
def answers(request, level=1):
    """Returns a render of answers.html"""
    context = RequestContext(request)
    cheat_message = '\\text{Ulovlig tegn har blitt brukt i svar}'
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            template = Template.objects.get(pk=form_values['primary_key'])
            if cheat_check(form_values['user_answer'], template.disallowed):
                return render_to_response('answers.html', {'answer': cheat_message}, context)
            context_dict = make_answer_context_dict(form_values)
            if request.is_ajax():
                change_level_rating(template, request.user, context_dict['user_won'], form_values['template_type'], level)
                print(3)
                return render_to_response('game/answer.html', context_dict, context)
            else:
                change_elo(template, request.user, context_dict['user_won'], form_values['template_type'])
            return render_to_response('answers.html', context_dict, context)
        else:
            print(form.errors)
    return render_to_response('answers.html')


@login_required
@user_passes_test(is_teacher, '/')
def templates(request):
    """Returns a render of tableview.html with all the templates"""
    panel_title = "Alle Maler"
    table = TemplateTable(Template.objects.filter(valid_flag=True))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def template_table_by_user(request):
    """Returns a render of tableview.html with only templates from the logged in user."""
    user = request.user
    panel_title = "Dine Maler"
    table = UserTemplatesTable(Template.objects.filter(creator=user))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def user_overview_table(request):
    """Returns a render of tableview.html with overview over users"""
    panel_title = "Brukere"
    table = UserTable(ExtendedUser.objects.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, "tableview.html", {"table": table, "panel_title": panel_title})


@login_required
@user_passes_test(is_teacher, '/')
def new_template(request):
    """Returns a render of newtemplate.html used for creating new templates"""
    context = RequestContext(request)
    # Retrieves a list of topics and passes them to the view.
    topics = ""
    for e in Topic.objects.all():
        topics += '§' + str(e.pk) + '§'
        topics += e.topic
    topics = topics[1:]
    context_dict = {'topics': topics}
    return render_to_response('newtemplate.html', context_dict, context)


@login_required
@user_passes_test(is_teacher, '/')
def edit_template(request, template_id):
    """Returns a render of edit.html used for editing existing templates"""
    context = RequestContext(request)
    context_dict = make_edit_context_dict(template_id)
    return render_to_response('edit.html', context_dict, context)


@login_required
def index(request):
    """Returns the index view with a list of topics"""
    list = Topic.objects.values_list('topic', flat=True)
    return render(request, "index.html", {"list": list})


### GAME ###
@login_required
def game(request, set_id):
    context = RequestContext(request)
    set_title = Set.objects.get(pk=set_id).name
    return render_to_response('game/screen.html', {'set_id': set_id, 'set_title': set_title}, context)


def chapters(request, set_id):
    if request.is_ajax():
        game_set = Set.objects.get(pk=set_id)
        set_chapters = game_set.chapters.all()
        context = RequestContext(request)
        medals = []
        completed = []
        chapter_progress(request.user, game_set, medals, completed)
        print('before return')
        return render_to_response('game/chapters.html',
                                  {'chapters': set_chapters, 'medals': json.dumps(medals),
                                   'completed': json.dumps(completed)}, context)
    else:
        return HttpResponseForbidden()


def levels(request, chapter_id):
    if request.is_ajax():
        game_chapter = Chapter.objects.get(pk=chapter_id)
        chapter_levels = game_chapter.levels.all()
        chapter_title = game_chapter.name
        context = RequestContext(request)
        progress_number = calculate_progress(request.user, game_chapter)
        star_per_level = get_stars_per_level(request.user, game_chapter)
        return render_to_response('game/levels.html',
                                  {'levels': chapter_levels, 'chapter_title': chapter_title,
                                   'progress_number': progress_number, 'spl': star_per_level}, context)
    else:
        return HttpResponseForbidden()

@login_required
def get_template(request, level_id):
    """Gets a template for a given level"""
    # if request.is_ajax():
    #   if request.method == 'GET':
    context = RequestContext(request)
    context_dict = generate_level(request.user, level_id)
    context_dict['rating'] = get_user_rating(request.user)

    return render_to_response('game/template.html', context_dict, context)


### SET, CHAPTER, LEVEL MANAGEMENT VIEWS ###

class SetsSearchView(SearchView):
    """ Search view for all set-type content """

    template_name = 'search/search.html'
    form_class = SetsSearchForm

    def get_queryset(self):
        queryset = super(SetsSearchView, self).get_queryset()
        return queryset

class SetSearch(SetsSearchView):
    title = 'set'
    extra_content = {'title':title }

def level_add_template(request, level_id, template_id):
    """Add a template fo a specified level"""
    response_data = {} # ajax response data
    level = Level.objects.get(pk=level_id)
    template = Template.objects.get(pk=template_id)
    if level.creator == request.user:
        level.templates.add(template)
        response_data['result'] = 'Template added to Level!'
        return HttpResponse("Template added to level!")
    else:
        return HttpResponse('You need to be the owner of the level you\'re editing!')


def add_template_to_current_level(request, template_id):
    """Add a template to the current level a teacher user is working on."""
    level = request.user.extendeduser.current_level
    template = Template.objects.get(pk=template_id)
    if level.creator == request.user:
        level.templates.add(template)
        return HttpResponse('Template added to level "'
                            + level.name +
                            '". (This will be a background process eventually.)')
    else:
        return HttpResponse('You need to be the owner of the level you\'re editing!')


def remove_template_from_current_level(request, template_id):
    """Remove a template from the current level a teacher user is working on."""
    level = request.user.extendeduser.current_level
    template = Template.objects.get(pk=template_id)
    if level.creator == request.user:
        level.templates.remove(template)
        return HttpResponse('Template removed from level "'
                        + level.name +
                        '". (This will be a background process eventually.)')
    else:
        return HttpResponse('Du må være eier a levelet for å legge til level')


def add_level_to_current_chapter(request, level_id):
    """Add a template to the current level a teacher user is working on."""
    chapter = request.user.extendeduser.current_chapter
    level = Template.objects.get(pk=level_id)
    if level.creator == request.user:
        chapter.levels.add(level)
        add_to_level_order = ''
        if chapter.level_order != '':
            add_to_level_order = ','
        chapter.level_order += add_to_level_order + level.pk
        return HttpResponse('Template added to level "'
                            + level.name +
                            '". (This will be a background process eventually.)')
    else:
        return HttpResponse('Du må være eier a kapitellet for å legge til level')


def preview_template(request, template_id):
    """Render a template to html"""
    #if request.is_ajax():
    q = Template.objects.get(pk=template_id)
    solution = str(q.question_text_latex.replace('\\\\', '\\')) + "\\n" + str(q.solution_latex.replace('\\\\', '\\'))

    return render_to_response('search/template_preview.html',
                              { 'solution': solution },
                              context_instance=RequestContext(request))


class SetCreateView(LoginRequiredMixin,CreateView):
    # form_class = SetForm
    model = Set
    fields = ['name', 'chapters',]
    template_name = 'sets/set_create_form.html'
    success_url = '/user/sets'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        return http.HttpResponseRedirect('/user/sets/')

def set_detail_view(request, set_id):
    """ List titles for all chapters, levels and templates in a set. """
    detailed_set = Set.objects.get(pk=set_id)
    set_chapters = detailed_set.chapters.all()
    #chapter_levels = set_chapters.levels.all()
    ## level_templates = chapter_levels.templates.all()
    set_title = detailed_set.name

    return render_to_response(
        'sets/user_set_details.html', { 'set' : detailed_set,
                                        'chapters': set_chapters,
                                        #'levels': chapter_levels, 'templates': level_templates,
                                        }, context_instance=RequestContext(request))


class UserSetListView(LoginRequiredMixin,ListView):
    template_name = 'sets/user_set_list.html'

    def get_queryset(self):
        return Set.objects.filter(creator=self.request.user)

    #def get_context_data(self, **kwargs):
    #    context = super(UserSetListView, self).get_context_data(**kwargs)
    #    context['now'] = datetime.datetime ???


@login_required
class ChapterCreate(LoginRequiredMixin,CreateView):
    model = Chapter
    fields = ['name', 'level']
    template_name = 'sets/chapter_create_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ChapterCreate, self).form_valid(form)


class SetChapterListView(LoginRequiredMixin,ListView):
    """List Chapters in Set"""
    template_name = 'sets/set_chapter_list.html'

    def get_queryset(self):
        self.set = get_object_or_404(Set, id=self.args[0])
        return self.set.chapters.all()

    def get_context_data(self, **kwargs):
        context = super(SetChapterListView, self).get_context_data(**kwargs)
        context['set'] = self.set
        return context


class ChapterLevelsListView(LoginRequiredMixin,ListView):
    """List levels in chapter"""
    template_name = 'sets/chapter_level_list.html'

    def get_queryset(self):
        self.chapter = get_object_or_404(Chapter, id=self.args[0])
        return self.chapter.levels.all()

    def get_context_data(self, **kwargs):
        context = super(ChapterLevelsListView, self).get_context_data(**kwargs)
        context['chapter'] = self.chapter
        return context


class LevelsTemplatesListView(LoginRequiredMixin, ListView):
    """List templates in level"""
    template_name = 'sets/level_template_list.html'

    def get_queryset(self):
        self.level = get_object_or_404(Level, id=self.args[0])
        return self.level.templates.all()

    def get_context_data(self, **kwargs):
        context = super(LevelsTemplatesListView, self).get_context_data(**kwargs)
        context['level'] = self.level
        return context


def manage_chapters(request):
    # Mass edit chapter names. (( Testing formsets ))
    # Should take a set PK to batch-edit chapter names in set or mass add inital chapters to a new set
    ChapterNameFormSet = formset_factory(ChapterNameForm, extra=9)
    if request.method == 'POST':
        formset = ChapterNameFormSet(request.post)
        if formset.is_valid():
            pass
    else:
        formset = ChapterNameFormSet()
    return render_to_response('sets/chapter_formset.html', {'formset': formset})


def manage_chapters_in_set(request, set_id):
    # Mass-edit chapters in a set. (( Testing formsets )) # todo: rework this to manage chapters by a logged in user
    # Should take a set PK to batch-edit chapter content in set or mass add inital empty chapters to a new set
    q = Set.objects.get(pk=set_id)
    ChapterNameInlineFormSet = inlineformset_factory(Set, Chapter, fields = ('name','levels'))
    if request.method == 'POST':
        formset = ChapterNameInlineFormSet(request.POST, instance=q)
        if formset.is_valid():
            formset.save()
            # mer her?
            return HttpResponse("WE DID IT REDDIT")
    else:
        formset = ChapterNameInlineFormSet(instance=q)
    return render_to_response('sets/chapter_formset.html', {'formset': formset, })


@login_required
class LevelCreateView(LoginRequiredMixin, CreateView):
    form_class = LevelCreateForm
    template_name = 'sets/level_create_form.html'

    # def form_valid(self, form):
    #    form.instance.creator = self.request.user
    #    return super(Level)


class UserCurrentSetsEdit(LoginRequiredMixin, UpdateView):
    model = ExtendedUser
    form_class = UserCurrentSetsForm
    #fields = ['current_set', 'current_chapter', 'current_level',]
    template_name = 'sets/user_current_sets_form.html'

    # todo: get these dang filters to work
    # def get_form_class(self, form_class=form_class):
    #    self.fields['current_level'].queryset = Level.objects.filter(creator=self.request.user.id)
    #    self.fields['current_chapter'].queryset = Chapter.objects.filter(creator=self.request.user.id)
    #    self.fields['current_set'].queryset = Set.objects.filter(creator=self.request.user.id)

    def get_object(self, queryset=None):
        obj = ExtendedUser.objects.get(user=self.request.user)
        return obj

    def get_success_url(self):
        success_url = self.request.GET.get('next', '')
        #success_url = self.request.get_full_path()
        return success_url