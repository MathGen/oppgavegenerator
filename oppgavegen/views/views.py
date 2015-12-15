"""

Defines views, and renders data to html templates.

"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.db.models import Count
from django.views.decorators.cache import cache_control
from haystack.generic_views import SearchView

from oppgavegen.views.sortable_listview import SortableListView
from oppgavegen.views.login_required_mixin import LoginRequiredMixin
from oppgavegen.templatetags.app_filters import is_teacher
from oppgavegen.view_logic.rating import change_elo, change_level_rating, get_user_rating
from oppgavegen.generation_folder.generation import generate_task
from oppgavegen.view_logic.submit_and_answer import *
from oppgavegen.view_logic.statistics import *
from oppgavegen.view_logic.add_remove import make_copy, remove_template_from_level
from oppgavegen.forms import *


@login_required
def index(request):
    """ The application front page. Shows a lists of Sets ordered by popularity or creation date. """
    context = {}
    sets = Set.objects.all().filter(is_public=True)
    user_sets = request.user.sets_joined.all()
    context['popular'] = sets.annotate(num_users=Count('users')).order_by('-num_users')[:20]
    context['latest'] = sets.order_by('-creation_date')[:20]
    context['user_sets'] = user_sets
    return render(request, "index.html", context)


@login_required
@user_passes_test(is_teacher, '/')
def new_template(request):
    """Returns a render of edit.html used for creating new templates"""
    context = RequestContext(request)
    # Retrieves a list of topics and passes them to the view.
    return render_to_response('template_editor.html', context)


@login_required
@user_passes_test(is_teacher, '/')
def edit_template(request, template_id):
    """Returns a render of edit.html used for editing existing templates"""
    context = RequestContext(request)
    template = Template.objects.get(pk=template_id)
    if template.editor == request.user:
        context_dict = make_edit_context_dict(template_id)
        return render_to_response('template_editor.html', context_dict, context)
    else:
        # If the user is not listed as the template editor open dialogue to confirm template cloning
        context_dict = {}
        context_dict['template'] = template
        return render_to_response('sets/confirm_template_copy.html', context_dict, context)

@login_required
@user_passes_test(is_teacher, '/')
def delete_template(request, template_id):
    """ Get a template, delete all relations and the template itself. """
    go_to = redirect('user_templates_list')
    context = RequestContext(request)
    query = Template.objects.filter(id__exact=template_id).prefetch_related('levels') #use filter to prefetch any levels
    template = query[0] #get the template from the query
    if template.editor == request.user:
        if template.levels.exists(): # check if any template->level relations exist
            # get the (single) level. there should be no possible way for a template to belong to several levels
            # unless the level has been defined via the admin interface
            level = template.levels.all()[0]
            remove_template_from_level(level_id=level.id,template_id=template_id, user=request.user)
        template.delete()
    else:
        go_to = redirect(index)
    return go_to


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required
def task(request):
    """Returns a render of taskview.html with a rating appropriate math problem"""
    context = RequestContext(request)
    question_type = request.GET.get('q', '')
    if question_type != "":
        context_dict = generate_task(request.user, question_type)
    else:
        context_dict = generate_task(request.user, "")
    context_dict['rating'] = get_user_rating(request.user)
    return render_to_response('taskview.html', context_dict, context)


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)  # Doesn't cache the page
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

            context_dict = make_answer_context_dict(form_values)

            if (cheat_check(user_answer, disallowed, form_values['variable_dictionary'].split('§'))) and \
                    (form_values['template_type'] == 'normal') and (context_dict['user_won']):
                context_dict['answer'] = cheat_message
                return render_to_response(render_to, context_dict, context)
            elif (required_check(user_answer, required, form_values['variable_dictionary'].split('§'))) and \
                    (form_values['template_type'] == 'normal') and (context_dict['user_won']):
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
@user_passes_test(is_teacher, '/')
def confirm_template_copy(request, template_id, goto_next="edit"):
    """ On template clone confirm, either go to editing the cloned template, or return to a list of the users templates """
    original_template = Template.objects.get(pk=template_id)
    new_template = make_copy(original_template, request.user)
    if goto_next == "edit":
        url = '/edit/' + str(new_template.id)
        go_to = redirect(url)
    else:
        go_to = redirect('user_templates_list')
    return go_to


class MiniSearchView(SearchView):
    template_name = 'search/compact_search.html'


def preview_template(request, template_id):
    """Return a template as JSON-object"""
    dict = {}
    q = Template.objects.get(pk=template_id)
    dict['template_text'] = str(q.question_text_latex.replace('\\\\', '\\'))
    dict['template_solution'] = str(q.solution_latex.replace('\\\\', '\\'))
    return JsonResponse(dict)


class TemplatesListView(LoginRequiredMixin, SortableListView):
    queryset = Template.objects.filter(copy=False)
    default_sort_field = 'id'
    panel_title = "Alle maler"
    include_copies = False

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
    paginate_by = 20
    paginate_orphans = 3
    context_object_name = 'template_list'

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
        context['include_copies'] = self.include_copies
        return context


class UserTemplatesListView(TemplatesListView):
    """ Renders a list of the logged in user's templates """
    queryset = Template.objects.all()
    panel_title = "Mine Maler"
    default_sort_field = 'id'
    include_copies = True

    allowed_sort_fields = (
        (default_sort_field, {'default_direction': '-', 'verbose_name': 'Dato'}),
        ('name', {'default_direction': '', 'verbose_name': 'Tittel'}),
        ('rating', {'default_direction': '-', 'verbose_name': 'Hovedrating'}),
        ('choice_rating', {'default_direction': '-', 'verbose_name': 'Flervalgsrating'}),
        ('fill_rating', {'default_direction': '-', 'verbose_name': 'Utfyllingsrating'}),
    )

    def get_queryset(self):
        qs = super(SortableListView, self).get_queryset()
        qs = qs.order_by(self.sort)
        return qs.filter(editor=self.request.user)


class UserTemplatesListViewNoCopies(UserTemplatesListView):
    """ Renders a list of the logged in user's templates. Does not display copies """
    queryset = Template.objects.all().filter(copy=False)
    panel_title = "Mine Maler (kun originale)"
    default_sort_field = 'id'
    include_copies = False


class UserSettingsView(UpdateView):
    form_class = NamedUserDetailsForm
    model = User
    template_name = 'registration/account_details.html'
    success_url = '/user/settings'

    def get_object(self, queryset=None):
        return self.request.user


def user_deactivate(request):
    # TODO: Unfinished. Users will have to be manually deactivated by an admin.
    return render(request, 'registration/user_deactivate_account.html')
