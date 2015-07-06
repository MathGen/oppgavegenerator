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
from oppgavegen.models import Set, Chapter, Level, Template, UserLevelProgress
from oppgavegen.view_logic.rating import change_elo, change_level_rating, get_user_rating
from oppgavegen.generation_folder.generation import generate_task, generate_level
from oppgavegen.view_logic.progress import calculate_progress, chapter_progress, get_stars_per_level, \
    get_user_rating_for_level, get_user_stars_for_level, check_for_level_skip
from oppgavegen.view_logic.view_logic import *
from oppgavegen.view_logic.current_work import *

# Search Views and Forms
from haystack.generic_views import SearchView
from oppgavegen.forms import QuestionForm, TemplateForm, LevelCreateForm, ChapterNameForm, UserCurrentSetsForm, SetsSearchForm
from django.forms.formsets import formset_factory
from django import http
from django.forms.models import inlineformset_factory

# Pre-defined renders of add/remove-buttons for toggle-action views
add_button = render_to_response('search/includes/add_button_ajax.txt')
remove_button = render_to_response('search/includes/remove_button_ajax.txt')


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
def submit(request):
    """Returns a render of submit html. Different depending on if the submission goes through ot not"""
    message = 'don\'t come here'
    if request.method == 'POST':
        message = 'Det har skjedd noe feil ved innsending av form'
        form = TemplateForm(request.POST)
        if form.is_valid():
            newtags = form.cleaned_data['tags_list']
            template = form.save(commit=False)
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
    required_message = '\\text{Svaret ditt har ikke utfylt alle krav}'
    render_to = 'answers.html'
    if request.is_ajax():
        render_to = 'game/answer.html'

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form_values = form.process()
            template = Template.objects.get(pk=form_values['primary_key'])

            user_answer = form_values['user_answer']
            try:
                disallowed = json.loads(template.disallowed)
            except ValueError:
                disallowed = []

            try:
                required = json.loads(template.required)
            except ValueError:
                required = []

            if cheat_check(user_answer, disallowed, form_values['variable_dictionary'].split('§')):
                return render_to_response(render_to, {'answer': cheat_message}, context)
            if required_check(user_answer, required, form_values['variable_dictionary'].split('§')):
                return render_to_response(render_to, {'answer': required_message}, context)

            context_dict = make_answer_context_dict(form_values)
            if request.is_ajax():

                new_user_rating, new_star = change_level_rating(template, request.user, context_dict['user_won'],
                                                                form_values['template_type'], level)

                context_dict['ulp'] = int(new_user_rating)
                context_dict['new_star'] = new_star
                context_dict['stars'] = get_user_stars_for_level(request.user, Level.objects.get(pk=level))
                return render_to_response(render_to, context_dict, context)
            else:
                change_elo(template, request.user, context_dict['user_won'], form_values['template_type'])
            return render_to_response(render_to, context_dict, context)
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
    return render_to_response('newtemplate.html', context)


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
    return render(request, "index.html")


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
        medals = [] # Both lists get updated in chapter_progress
        completed = []
        progress_number = chapter_progress(request.user, game_set, medals, completed)
        order = game_set.order
        set_chapters_ordered = []

        for x in order.split(','):
            for chapter in set_chapters:
                if chapter.pk == int(x):
                    set_chapters_ordered.append(chapter)
                    break

        return render_to_response('game/chapters.html',
                                  {'chapters': set_chapters_ordered, 'medals': json.dumps(medals),
                                   'completed': json.dumps(completed), 'progress_number': progress_number}, context)
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

        order = game_chapter.order
        chapter_levels_ordered = []

        for x in order.split(','):
            for chapter in chapter_levels:
                if chapter.pk == int(x):
                    chapter_levels_ordered.append(chapter)
                    break

        return render_to_response('game/levels.html',
                                  {'levels': chapter_levels_ordered, 'chapter_title': chapter_title,
                                   'progress_number': progress_number, 'spl': star_per_level, 'chapter_id': chapter_id}
                                   ,context)
    else:
        return HttpResponseForbidden()

@login_required
def get_template(request):
    """Gets a template for a given level"""
    # if request.is_ajax():
    #   if request.method == 'GET':
    context = RequestContext(request)
    context_dict = {'message': 'Noe har gått feil.'}
    if request.method == 'POST':
        form = request.POST
        print(form)
        level_id = int(form['level_id[]'])
        print(level_id)
        chapter_id = int(form['chapter_id'])
        if check_for_level_skip(request.user, Chapter.objects.get(pk=chapter_id), level_id):
            return render_to_response('game/template.html', context_dict, context)
        context_dict = generate_level(request.user, level_id)
        context_dict['rating'] = get_user_rating(request.user)
        level = Level.objects.get(pk=level_id)
        context_dict['stars'] = get_user_stars_for_level(request.user, level)
        context_dict['ulp'] = get_user_rating_for_level(request.user, level)

    return render_to_response('game/template.html', context_dict, context)


### SET, CHAPTER, LEVEL MANAGEMENT VIEWS ###
@login_required
def set_edit(request, set_id=""):
    context = RequestContext(request)
    set_title = ""
    chapters = []
    if set_id:
        edit_set = Set.objects.get(pk=set_id)
        set_current_set(request.user, edit_set)
        set_title = edit_set.name
        order = edit_set.order

        for x in order.split(','):
            for chapter in edit_set.chapters.all():
                if chapter.pk == int(x):
                    chapters.append(chapter)
                    break
    return render_to_response('sets/container.html', {'set_id': set_id, 'chapters': chapters,
                                                      'set_edit': True, 'set_title': set_title}, context)


def chapter_edit(request, chapter_id=""):
    context = RequestContext(request)
    chapter_title = ""
    levels = []
    if chapter_id:
        edit_chapter = Chapter.objects.get(pk=chapter_id)
        set_current_chapter(request.user, edit_chapter)
        chapter_title = edit_chapter.name
        order = edit_chapter.order

        for x in order.split(','):
            for level in edit_chapter.levels.all():
                if level.pk == int(x):
                    levels.append(level)
                    break
    return render_to_response('sets/container.html', {'chapter_id': chapter_id, 'levels': levels,
                                                      'chapter_edit': True, 'chapter_title': chapter_title}, context)


def level_edit(request, level_id=""):
    context = RequestContext(request)
    get_templates = ""
    level_title = ""
    k_factor = 3
    if level_id:
        edit_level = Level.objects.get(pk=level_id)
        set_current_level(request.user, edit_level)
        level_title = edit_level.name
        k_factor = edit_level.k_factor
        get_templates = edit_level.templates.all()
    return render_to_response('sets/container.html', {'level_id': level_id, 'templates': get_templates,
                                                      'level_edit': True, 'level_title': level_title,
                                                      'k_factor': k_factor}, context)


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


class MiniSearchView(SearchView):
    template_name = 'search/mini_search.html'


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


def toggle_template_level(request, template_id):
    """"
    Render a button to either add or remove a template to/from a level.
    For Haystack Search-results.
    """
    level = request.user.extendeduser.current_level
    try:
        template = Template.objects.get(pk=template_id)
    except Template.DoesNotExist as e:
        raise ValueError("Unknown template.id=" + str(template_id) + "or level.id=" +
                         str(level.id) + ". Original error: " + str(e))
    if template in level.templates.all():
        level.templates.remove(template)
        level.save()
        button = add_button
    else:
        level.templates.add(template)
        button = remove_button
    return button


def toggle_chapter_level(request, level_id):
    """"
    Render a button to either add or remove a level to/from a chapter.
    For Haystack Search-results.
    """
    chapter = request.user.extendeduser.current_chapter
    try:
        level = Template.objects.get(pk=level_id)
    except Template.DoesNotExist as e:
        raise ValueError("Unknown level.id=" + str(level_id) + "or chapter.id=" +
                         str(chapter.id) + ". Original error: " + str(e))
    if level in chapter.levels.all():
        level.templates.remove(level)
        chapter.save()
        button = add_button
    else:
        chapter.levels.add(level)
        button = remove_button
    return button


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



def preview_template(request, template_id):
    """Render a template to html"""
    #if request.is_ajax():
    q = Template.objects.get(pk=template_id)
    solution = str(q.question_text_latex.replace('\\\\', '\\')) + "\\n" + str(q.solution_latex.replace('\\\\', '\\'))

    return render_to_response('search/template_preview.html',
                              { 'solution': solution },
                              context_instance=RequestContext(request))


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


class UserCurrentSetsEdit(LoginRequiredMixin, UpdateView):
    model = ExtendedUser
    form_class = UserCurrentSetsForm
    #fields = ['current_set', 'current_chapter', 'current_level',]
    template_name = 'sets/user_current_sets_form.html'

    def get_object(self, queryset=None):
        obj = ExtendedUser.objects.get(user=self.request.user)
        return obj

    def get_success_url(self):
        success_url = self.request.GET.get('next', '')
        #success_url = self.request.get_full_path()
        return success_url

    # todo: filter dropdowns for objects made by current user
    # class based views are weird about this
    # def get_form_class(self, form_class=form_class):
    #     form_class.fields['current_level'].queryset = Level.objects.filter(creator=self.request.user)
    #     form_class.fields['current_chapter'].queryset = Chapter.objects.filter(creator=self.request.user)
    #     #self.fields['current_chapter'].queryset = Chapter.objects.filter(creator=self.request.user)
    #     #self.fields['current_set'].queryset = Set.objects.filter(creator=self.request.user)
    #     return form_class

def refresh_navbar(request):
    return render_to_response('includes/current_sets_snippet.html')

def level_stats(request, level_id):
    """
    Prepares rating statistics for a level by counting student level ratings within specific intervals.
    Designed with morris.js bar chart in mind (see charts.html)
    The range is from 0 to 2400, and the measuring interval is 100 counting from 1100 and up.
    """

    dict = {}
    level = Level.objects.get(pk=level_id)
    dict['level_name'] = level.name
    stats = level.student_progresses.all()

    # amount of students in intervals
    interval1 = 0  # 0-800
    interval2 = 0  # 800-1100
    interval3 = 0  # 1100-1200
    interval4 = 0  # 1200-1300
    interval5 = 0  # 1300-1400
    interval6 = 0  # 1400-1500
    interval7 = 0  # 1500-1600
    interval8 = 0  # 1600-1700
    interval9 = 0  # 1700-1800
    interval10 = 0 # 1800-1900
    interval11 = 0 # 1900-2000
    interval12 = 0 # 2000-2100
    interval13 = 0 # 2100-2200
    interval14 = 0 # 2200-2300
    interval15 = 0 # 2300-2400
    other = 0      # out of range somehow (just in case)

    ratings = [] # list of all ratings

    for e in stats:
        if 0 <= e.level_rating <= 800:
            interval1 += 1
        elif 801 <= e.level_rating <= 1100:
            interval2 += 1
        elif 1101 <= e.level_rating <= 1200:
            interval3 += 1
        elif 1201 <= e.level_rating <= 1300:
            interval4 += 1
        elif 1301 <= e.level_rating <= 1400:
            interval5 += 1
        elif 1401 <= e.level_rating <= 1500:
            interval6 += 1
        elif 1501 <= e.level_rating <= 1600:
            interval7 += 1
        elif 1601 <= e.level_rating <= 1700:
            interval8 += 1
        elif 1701 <= e.level_rating <= 1800:
            interval9 += 1
        elif 1801 <= e.level_rating <= 1900:
            interval10 += 1
        elif 1901 <= e.level_rating <= 2000:
            interval11 += 1
        elif 2001 <= e.level_rating <= 2100:
            interval12 += 1
        elif 2101 <= e.level_rating <= 2200:
            interval13 += 1
        elif 2201 <= e.level_rating <= 2300:
            interval14 += 1
        elif 2301 <= e.level_rating <= 2400:
            interval15 += 1
        else:
            other += 1

    for e in stats:
        ratings.append(e.level_rating)
    if ratings:
        dict['players'] = len(ratings)
        dict['average'] = int(sum(ratings)/len(ratings))
    dict['entries'] = [interval1, interval2, interval3, interval4, interval5, interval6, interval7, interval8,
                       interval9,interval10, interval11, interval12, interval13, interval14, interval15]
    return render(request, 'sets/charts.html', dict)
