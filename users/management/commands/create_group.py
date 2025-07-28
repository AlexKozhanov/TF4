from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_group, created = Group.objects.get_or_create(name="Пользователи")
        users_group.permissions.add(25, 26, 27, 28, 29, 30, 31, 32)
        self.stdout.write(self.style.SUCCESS(f'Создана группа {users_group}'))
