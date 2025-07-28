from django.urls import path
from diary.apps import DiaryConfig
from diary.views import (
    Home, DiaryListView, DiaryDetailListView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView,
    DiaryEntriesListView, DiaryEntriesDetailListView, DiaryEntriesCreateView, DiaryEntriesUpdateView, SearchDiary,
    SearchDiaryEntries, EntriesByDiaryListView, DiaryEntriesDeleteView)

app_name = DiaryConfig.name

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('diary/', DiaryListView.as_view(), name='diary_list'),
    path('diary/<int:pk>/', DiaryDetailListView.as_view(), name='diary_detail'),
    path('diary/new', DiaryCreateView.as_view(), name='diary_create'),
    path('diary/<int:pk>/update', DiaryUpdateView.as_view(), name='diary_update'),
    path('diary/<int:pk>/delete', DiaryDeleteView.as_view(), name='diary_delete'),
    path('diary/searchdiary/', SearchDiary.as_view(), name='diary_search'),

    path('diary/entries/', DiaryEntriesListView.as_view(), name='entries_list'),
    path('diary/entries/<int:pk>/', DiaryEntriesDetailListView.as_view(), name='entries_detail'),
    path('diary/entries/new', DiaryEntriesCreateView.as_view(), name='entries_create'),
    path('diary/entries/<int:pk>/update', DiaryEntriesUpdateView.as_view(), name='entries_update'),
    path('diary/entries/<int:pk>/delete', DiaryEntriesDeleteView.as_view(), name='entries_delete'),
    path('diary/entries/searchdiaryentries/', SearchDiaryEntries.as_view(), name='entries_search'),

    path('diary/list/<int:diary_id>/', EntriesByDiaryListView.as_view(), name='entries_diary'),]
