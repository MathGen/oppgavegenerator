"""

Defines views, and renders data to html templates.

"""

import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from oppgavegen.utility.sortable_listview import SortableListView

from django.views.decorators.cache import cache_control

from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen.models import Set, Chapter, Level, Template
from oppgavegen.view_logic.rating import change_elo, change_level_rating, get_user_rating
from oppgavegen.generation_folder.generation import generate_task, generate_level
from oppgavegen.view_logic.progress import calculate_progress, chapter_progress, get_stars_per_level, \
    get_user_rating_for_level, get_user_stars_for_level, check_for_level_skip
from oppgavegen.view_logic.view_logic import *
from oppgavegen.view_logic.current_work import *
from oppgavegen.view_logic.statistics import *

from registration.views import RegistrationView

# Search Views and Forms
from haystack.forms import SearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from oppgavegen.forms import *

# Pre-defined renders of add/remove-buttons for toggle-action views
add_button = render_to_response('search/includes/add_button_ajax.html')
remove_button = render_to_response('search/includes/remove_button_ajax.html')


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


class MathGenRegistrationView(RegistrationView):
    form_class = NamedUserRegistrationForm


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
            print('wth')


            context_dict = make_answer_context_dict(form_values)

            if cheat_check(user_answer, disallowed, form_values['variable_dictionary'].split('§')) and \
                    not (form_values['template_type'] == 'multiple' and context_dict['user_won']):
                context_dict['answer'] = cheat_message
                return render_to_response(render_to, context_dict, context)
            if required_check(user_answer, required, form_values['variable_dictionary'].split('§')) and \
                    not (form_values['template_type'] == 'multiple' and context_dict['user_won']):
                context_dict['answer'] = required_message
                return render_to_response(render_to, context_dict, context)


            if request.is_ajax():
                new_user_rating, new_star = change_level_rating(template, request.user, context_dict['user_won'],
                                                                form_values['template_type'], level)
                context_dict['chapter_id'] = request.POST['chapter_id']
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
def new_template(request):
    """Returns a render of edit.html used for creating new templates"""
    context = RequestContext(request)
    # Retrieves a list of topics and passes them to the view.
    return render_to_response('edit.html', context)


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
                                   'completed': json.dumps(completed), 'progress_number': progress_number,
                                   'set_id': set_id}, context)
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
                                   'progress_number': progress_number, 'spl': star_per_level, 'chapter_id': chapter_id},
                                  context)
    else:
        return HttpResponseForbidden()

@login_required
def get_template(request):
    """Gets a template for a given level"""
    # if request.is_ajax():
    #   if request.method == 'GET':
    try:
        context = RequestContext(request)
        context_dict = {'message': 'Noe har gått feil.'}
        if request.method == 'POST':
            form = request.POST
            print(form)
            level_id = int(form['level_id[]'])
            print(level_id)
            chapter_id = int(form['chapter_id'])
            #if check_for_level_skip(request.user, Chapter.objects.get(pk=chapter_id), level_id):
            #    return render_to_response('game/template.html', context_dict, context)
            context_dict = generate_level(request.user, level_id)
            context_dict['rating'] = get_user_rating(request.user)
            level = Level.objects.get(pk=level_id)
            context_dict['stars'] = get_user_stars_for_level(request.user, level)
            context_dict['ulp'] = get_user_rating_for_level(request.user, level)

        return render_to_response('game/template.html', context_dict, context)
    except Exception as e:
        print(e)


### SET, CHAPTER, LEVEL MANAGEMENT VIEWS ###
@login_required
def set_list(request):
    context = RequestContext(request)
    context_dict = {'set_list': True}
    render_to = 'sets/container.html'

    sets = Set.objects.all().filter(editor=request.user)
    context_dict['sets'] = sets

    return render_to_response(render_to, context_dict, context)

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
    """Return a template as JSON-object"""
    dict = {}
    q = Template.objects.get(pk=template_id)
    dict['template_text'] = str(q.question_text_latex.replace('\\\\', '\\'))
    dict['template_solution'] = str(q.solution_latex.replace('\\\\', '\\'))
    return JsonResponse(dict)

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


class TemplatesListView(LoginRequiredMixin,SortableListView):
    queryset = Template.objects.filter(copy=False)
    default_sort_field = 'creation_date'
    panel_title = "Alle maler"

    allowed_sort_fields = (
        (default_sort_field, {'default_direction': '-', 'verbose_name': 'Dato'}),
        ('name', {'default_direction': '', 'verbose_name': 'Tittel'}),
        ('editor', {'default_direction': '', 'verbose_name': 'Forfatter'}),
        ('rating', {'default_direction': '-', 'verbose_name': 'Hovedrating'}),
        ('choice_rating', {'default_direction': '-', 'verbose_name': 'Flervalgsrating'}),
        ('fill_rating', {'default_direction': '-', 'verbose_name': 'Utfyllingsrating'}),
    )

    template_name = 'template_list.html'
    allow_empty = True
    paginate_by = 15
    paginate_orphans = 20
    context_object_name = 'template_list'
    model = Template

    def get_queryset(self):
        qs = super(SortableListView, self).get_queryset()
        qs = qs.order_by(self.sort)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SortableListView,
                        self).get_context_data(**kwargs)
        context['current_sort_query'] = self.get_sort_string()
        context['current_querystring'] = self.get_querystring()
        context['sort_link_list'] = self.sort_link_list
        context['panel_title'] = self.panel_title
        return context

class UserTemplatesListView(TemplatesListView):
    #queryset = Template.objects.all()
    panel_title = "Mine Maler"
    default_sort_field = 'creation_date'

    allowed_sort_fields = (
        (default_sort_field, {'default_direction': '-', 'verbose_name': 'Dato'}),
        ('name', {'default_direction': '', 'verbose_name': 'Tittel'}),
        ('rating', {'default_direction': '-', 'verbose_name': 'Hovedrating'}),
        ('choice_rating', {'default_direction': '-', 'verbose_name': 'Flervalgsrating'}),
        ('fill_rating', {'default_direction': '-', 'verbose_name': 'Utfyllingsrating'}),
    )

    def get_queryset(self):
        #qs = super(UserTemplatesListView, self).get_queryset()
        #qs.filter(creator=self.request.user)
        qs = Template.objects.order_by(self.sort).filter(editor=self.request.user)
        return qs


class UserTemplatesSearchView(SearchView):
    template_name = 'search/template_search.html'
    queryset = SearchQuerySet()

class UserSetListView(LoginRequiredMixin,ListView):
    template_name = 'sets/user_set_list.html'

    def get_queryset(self):
        return Set.objects.filter(creator=self.request.user)

class SetChapterListView(LoginRequiredMixin,ListView):
    """List Chapters in Set"""
    template_name = 'sets/set_chapter_list.html'

    def get_queryset(self):
        chapters = []
        self.set = get_object_or_404(Set, id=self.args[0])
        order = self.set.order

        for x in order.split(','):
            for chapter in self.set.chapters.all():
                if chapter.pk == int(x):
                    chapters.append(chapter)
                    break
        return chapters

    def get_context_data(self, **kwargs):
        context = super(SetChapterListView, self).get_context_data(**kwargs)
        context['set'] = self.set
        set_current_set(self.request.user, self.set)
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
        set_current_chapter(self.request.user, self.chapter)
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
        set_current_level(self.request.user, self.level)
        context['k_factor'] = self.level.k_factor
        return context


class UserCurrentSetsEdit(LoginRequiredMixin, UpdateView):
    template_name = 'sets/user_current_sets_form.html'

    def get_object(self, queryset=None):
        obj = ExtendedUser.objects.get(user=self.request.user)
        return obj

    def get_form_class(self):
        form = UserCurrentSetsForm
        form.current_set.queryset = Set.objects.all().filter(editor=self.request.user)
        form.current_chapter.queryset = Chapter.objects.all().filter(editor=self.request.user)
        form.current_level.queryset = Level.objects.all().filter(editor=self.request.user)
        return form

    def get_success_url(self):
        success_url = self.request.GET.get('next', '')
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
    return render(request,'includes/current_sets_snippet.html')

def refresh_user_sets(request):
    context = {}
    context['object_list'] = Set.objects.get(editor=request.user)
    return render(request,'sets/includes/set_list.html', context)

def level_stats(request, level_id):
    """
    Prepares rating statistics for a level by counting student level. / template-ratings within specific intervals.
    Designed with morris.js bar chart in mind (see charts.html)
    The range is from 0 to 2400, and the measuring interval is 100 counting from 1100 and up.
    """

    context_dict = {}
    level = Level.objects.get(pk=level_id)
    context_dict['level_name'] = level.name
    stats = level.student_progresses.all()

    studentratings = stats.values_list('level_rating', flat=True) # list of all ratings

    if studentratings:
        context_dict['players'] = len(studentratings)
        context_dict['average'] = int(sum(studentratings)/context_dict['players'])

    context_dict['student_entries'] = get_level_student_statistics(level)
    context_dict['templates'] = level.templates.exists()
    context_dict['template_entries'] = get_level_template_statistics(level)
    context_dict['template_original'] = get_level_template_original_statistics(level)
    return render(request, 'sets/charts.html', context_dict)

class UserSettingsView(UpdateView):
    form_class = NamedUserDetailsForm
    model = User
    template_name = 'registration/account_details.html'
    success_url = '/user/settings'

    def get_object(self, queryset=None):
        return self.request.user


def user_deactivate(request):
    return render(request, 'registration/user_deactivate_account.html')
