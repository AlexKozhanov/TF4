from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.shortcuts import (render, get_object_or_404, redirect)
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import (
    TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView, )

# CACHE
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

# Object Diary
from diary.models import (Diary, DiaryEntries)
from diary.forms import (DiaryForm, DiaryEntriesForm)


# --- Main Menu ---
class Home(TemplateView):
    template_name = 'diary/home.html'


# --- contacts template---
class Contacts(TemplateView):
    template_name = 'diary/contacts.html'


# --- CRUD Diary ---
# @method_decorator(cache_page(60 * 15), name='dispatch')
class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diary_list.html'  # permission_required = 'catalog.view_product'


# @method_decorator(cache_page(60 * 15), name='dispatch')
class DiaryDetailListView(LoginRequiredMixin, DetailView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_detail.html'

    # def get_object(self, queryset=None):
    #     """ Счетчик просмотров """
    #     self.object = super().get_object(queryset)
    #     self.object.views_counter += 1
    #     self.object.save()
    #     return self.object


class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')

    # permission_required = 'catalog.add_product'

    def form_valid(self, form):
        user_diary = form.save()
        user_diary.owner = self.request.user
        user_diary.save()
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')

    # permission_required = 'catalog.change_product'

    def get_success_url(self):
        return reverse('diary:diary_detail', args=[self.kwargs.get('pk')])

    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.owner:
    #         return ProductForm
    #     if user.has_perm('catalog.can_unpublish_product'):
    #         return ProductModeratorForm
    #     raise PermissionDenied


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')  # permission_required = 'diary.delete_product'

    # def get_form_class(self):  #     user = self.request.user  #     if not user.has_perm('diary.delete_product') or not user == self.object.owner:  #         raise PermissionDenied


# --- CRUD DiaryEntries ---
class DiaryEntriesListView(LoginRequiredMixin, ListView):
    model = DiaryEntries
    template_name = 'diary/entries_list.html'  # permission_required = 'catalog.view_category'

    # def get_queryset(self):  #     queryset = cache.get('category_queryset')  #     if not queryset:  #         queryset = super().get_queryset()  #         cache.set('category_queryset', queryset, 60 * 15)  #     return queryset


class DiaryEntriesDetailListView(LoginRequiredMixin, DetailView):
    model = DiaryEntries
    template_name = 'diary/entries_detail.html'
    success_url = reverse_lazy('diary:entries_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object


class DiaryEntriesCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntries
    form_class = DiaryEntriesForm
    template_name = 'diary/entries_form.html'
    success_url = reverse_lazy('diary:entries_list')  # permission_required = 'diary.create_category'


class DiaryEntriesUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaryEntries
    form_class = DiaryEntriesForm
    template_name = 'diary/entries_form.html'
    success_url = reverse_lazy('diary:entries_list')  # permission_required = 'diary.change_category'

    # def get_success_url(self):  #     return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class DiaryEntriesDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaryEntries
    template_name = 'diary/entries_delete.html'
    success_url = reverse_lazy('diary:entries_list')  # permission_required = 'diary.delete_product'

    # def get_form_class(self):  #     user = self.request.user  #     if not user.has_perm('diary.delete_product') or not user == self.object.owner:  #         raise PermissionDenied
