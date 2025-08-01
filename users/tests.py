from rest_framework import status
from django.test import TestCase
from django.test.client import Client

from diary.models import Diary
from users.models import User


class DiaryTest(TestCase):
    """
    Тестирование модели User.
    """

    def setUp(self):
        """
        Создание данных перед тестированием.
        """
        # self.user_group = Group.objects.create(name="Пользователи")
        self.user = User.objects.create(email="test@test.ru", password='test123')
        self.user.is_superuser = True
        # self.user.groups.add(self.user_group)
        self.diary = Diary.objects.create(
            head="test дневник",
            content="test описание дневника",
            owner=self.user,
        )
        # self.client.force_authenticate(user=self.user)

    def test_1(self):
        """
        Авторизация.
        """
        c = Client()
        response = c.post('/users/login/',
                          {'email': 'test@test.ru',
                           'password': 'test123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
