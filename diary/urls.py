from django.urls import path
from diary.apps import DiaryConfig
from diary.views import (Home, Contacts, DiaryListView, DiaryDetailListView, DiaryCreateView, DiaryUpdateView,
    DiaryDeleteView, DiaryEntriesListView, DiaryEntriesDetailListView, DiaryEntriesCreateView, DiaryEntriesUpdateView)

app_name = DiaryConfig.name


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('diary/', DiaryListView.as_view(), name='product_list'),
    path('diary/<int:pk>/', DiaryDetailListView.as_view(), name='product_detail'),
    path('diary/new', DiaryCreateView.as_view(), name='product_create'),
    path('diary/<int:pk>/update', DiaryUpdateView.as_view(), name='product_update'),
    path('diary/<int:pk>/delete', DiaryDeleteView.as_view(), name='product_delete'),

    path('diary/entries/', DiaryEntriesListView.as_view(), name='category_list'),
    path('diary/entries/<int:pk>/', DiaryEntriesDetailListView.as_view(), name='category_detail'),
    path('diary/entries/new', DiaryEntriesCreateView.as_view(), name='category_create'),
    path('diary/entries/<int:pk>/update', DiaryEntriesUpdateView.as_view(), name='category_update'),
]