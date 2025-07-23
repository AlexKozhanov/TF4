from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_group, created = Group.objects.get_or_create(name="Пользователи")
        self.stdout.write(self.style.SUCCESS(f'Создана группа "Пользователи"'))
