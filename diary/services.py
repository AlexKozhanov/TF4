from diary.models import DiaryEntries


def get_products_in_category(diary_id):

    return DiaryEntries.objects.filter(diary_id=diary_id)
