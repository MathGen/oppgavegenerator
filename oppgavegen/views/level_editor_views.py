from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from oppgavegen.models import Set, Chapter, Level
from oppgavegen.views.login_required_mixin import LoginRequiredMixin
from oppgavegen.view_logic.current_work import set_current_set, set_current_chapter, set_current_level


class UserSetListView(LoginRequiredMixin, ListView):
    template_name = 'sets/user_set_list.html'

    def get_queryset(self):
        return Set.objects.filter(editor=self.request.user)


class SetChapterListView(LoginRequiredMixin, ListView):
    """List Chapters in Set"""
    template_name = 'sets/set_chapter_list.html'

    def get_queryset(self):
        chapters = []
        self.set = get_object_or_404(Set, id=self.args[0])
        order = self.set.order

        for x in order.split(','):  # get chapters in chapterlist in order
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


class ChapterLevelsListView(LoginRequiredMixin, ListView):
    """List levels in chapter"""
    template_name = 'sets/chapter_level_list.html'

    def get_queryset(self):
        levels = []
        self.chapter = get_object_or_404(Chapter, id=self.args[0])
        order = self.chapter.order

        for x in order.split(','):
            for level in self.chapter.levels.all():
                if level.pk == int(x):
                    levels.append(level)
                    break

        return levels


    def get_context_data(self, **kwargs):
        context = super(ChapterLevelsListView, self).get_context_data(**kwargs)
        context['chapter'] = self.chapter
        set_current_chapter(self.request.user, self.chapter)
        return context


@login_required
def set_public(request, set_id):
    """ Set a private or new set to be public (listed on the front page) """
    set = Set.objects.get(pk=set_id)
    if set.editor == request.user:
        set.is_public = True
        set.save()
        return redirect('chapters_by_set', set_id)
    else:
        return redirect('index')

@login_required
def set_private(request, set_id):
    """ Set a public set to be private (not listed on the front page) """
    set = Set.objects.get(pk=set_id)
    if set.editor == request.user:
        set.is_public = False
        set.save()
        return redirect('chapters_by_set', set_id)
    else:
        return redirect('index')


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
