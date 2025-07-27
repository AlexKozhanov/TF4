from django.core.management.base import BaseCommand
from diary.models import Diary, DiaryEntries
from users.models import User


class Command(BaseCommand):
    help = 'Добавление данных Дневника и Записей в БД'

    def handle(self, *args, **options):
        user = User.objects.get(mail='user1 @ example.com')
        data_diary = [
            {
                'head': 'Ежедневные мысли',
                'content': 'Здесь я буду записывать мысли за прошедшый день',
                'owner': user
            }
        ]
        MyDiary = Diary.objects.get(head='Ежедневные мысли')
        data_diaryentries = [
            {
                'head': 'Мысль1',
                'content': '01.01 - сегодня я думал  вечности',
                'owner': user,
                'diary': MyDiary,
                'publication_status': True
            },
            {
                'head': 'Мысль2',
                'content': '02.01 - сегодня я читал рассказ Дубровкий, захотелось посмотреть на огонь',
                'owner': user,
                'diary': MyDiary,
                'publication_status': True
            },
            {
                'head': 'Мысль2',
                'content': '03.01 - ничего не думал, не буду публиковать',
                'owner': user,
                'diary': MyDiary,
                'publication_status': False
            }
        ]

        for diary in data_diary:
            data_diary, created = Diary.objects.get_or_create(**diary)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added diary: {diary.head}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {diary.name}'))
        for diaryentries in data_diaryentries:
            diaryentries, created = DiaryEntries.objects.get_or_create(**diaryentries)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added diaryentries: {diaryentries.head}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {diaryentries.head}'))
