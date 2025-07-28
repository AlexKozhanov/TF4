from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import (
    TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView, )
from django.db.models import Q
# CACHE

# Object Diary
from diary.models import (Diary, DiaryEntries)
from diary.forms import (DiaryForm, DiaryEntriesForm)
from diary.services import get_products_in_category


# --- Main Menu ---
class Home(TemplateView):
    template_name = 'diary/home.html'


# --- contacts template---
class Contacts(TemplateView):
    template_name = 'diary/contacts.html'


# --- CRUD Diary ---
# @method_decorator(cache_page(60 * 15), name='dispatch')
class DiaryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    permission_required = 'diary.view_diary'


# @method_decorator(cache_page(60 * 15), name='dispatch')
class DiaryDetailListView(LoginRequiredMixin, DetailView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_detail.html'

    # def get_queryset(self):
    #     queryset = cache.get('category_queryset')
    #     if not queryset:
    #         queryset = super().get_queryset()
    #         cache.set('category_queryset', queryset, 60 * 15)
    #     return queryset


class DiaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')
    permission_required = 'diary.add_diary'

    def form_valid(self, form):
        user_diary = form.save()
        user_diary.owner = self.request.user
        user_diary.save()
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')
    permission_required = 'diary.change_diary'

    def get_success_url(self):
        return reverse('diary:diary_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return DiaryForm
    #     if user.has_perm('catalog.can_unpublish_product'):
    #         return ProductModeratorForm
        raise PermissionDenied


class DiaryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Diary
    # template_name = 'diary/diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')
    permission_required = 'diary.delete_diary'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


# --- CRUD DiaryEntries ---
class DiaryEntriesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DiaryEntries
    template_name = 'diary/entries_list.html'
    permission_required = 'diary.view_diaryentries'


class DiaryEntriesDetailListView(LoginRequiredMixin, DetailView):
    model = DiaryEntries
    template_name = 'diary/entries_detail.html'
    success_url = reverse_lazy('diary:entries_list')

    def get_object(self, queryset=None):
        """ Счетчик просмотров """
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class DiaryEntriesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DiaryEntries
    form_class = DiaryEntriesForm
    template_name = 'diary/entries_form.html'
    success_url = reverse_lazy('diary:entries_list')
    permission_required = 'diary.add_diaryentries'


class DiaryEntriesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DiaryEntries
    form_class = DiaryEntriesForm
    template_name = 'diary/entries_form.html'
    success_url = reverse_lazy('diary:entries_list')
    permission_required = 'diary.change_diaryentries'

    def get_success_url(self):
        return reverse('diary:entries_detail', args=[self.kwargs.get('pk')])


class DiaryEntriesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DiaryEntries
    # template_name = 'diary/diaryentries_confirm_delete.html'
    success_url = reverse_lazy('diary:entries_list')
    permission_required = 'diary.delete_diaryentries'

    # def get_form_class(self):
    #     user = self.request.user
    #     if not user.has_perm('diary.delete_diaryentries') or not user == self.object.owner_entries:
    #     # if not user == self.object.owner:
    #         raise PermissionDenied
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner_entries != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class EntriesByDiaryListView(ListView):
    template_name = 'diary/entries_diary.html'
    context_object_name = 'productsbycategory'

    def get_queryset(self):
        diary_id = self.kwargs['diary_id']
        return get_products_in_category(diary_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diary_id = self.kwargs['diary_id']
        context['diary'] = Diary.objects.get(pk=diary_id)
        return context


class SearchDiary(ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'diary'
    paginate_by = 5

    def get_queryset(self):
        return Diary.objects.filter(
            Q(head__icontains=self.request.GET.get('q')) | Q(content__icontains=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class SearchDiaryEntries(ListView):
    model = DiaryEntries
    template_name = 'diary/entries_list.html'
    context_object_name = 'entries'
    paginate_by = 5

    def get_queryset(self):
        # return Diary.objects.filter(content__icontains=self.request.GET.get('q'))
        return DiaryEntries.objects.filter(
            Q(head__icontains=self.request.GET.get('q')) | Q(content__icontains=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context
