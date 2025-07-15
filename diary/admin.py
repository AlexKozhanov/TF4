from django.contrib import admin
from diary.models import Diary, DiaryEntries


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'head', 'content', 'owner')
    list_filter = ('head',)
    search_fields = ('head',)


@admin.register(DiaryEntries)
class DiaryEntriesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DiaryEntries._meta.fields]
    list_filter = ('head',)
    search_fields = ('head',)
