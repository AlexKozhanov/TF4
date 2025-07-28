from rest_framework import status
from django.test import TestCase
from django.test.client import Client

from diary.models import Diary
from users.models import User


class DiaryTest(TestCase):
    """
    Тестирование модели Diary.
    CRUD дневника.
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

    # def test_list_diary(self):
    #     """
    #     Тест вывод всех дневников.
    #     """
    #     c = Client()
    #     response = c.post('/users/login/', self.user)
    #     url = reverse('diary:diary_list')
    #     response = self.client.get(url)
    #     # response = self.client.get(
    #     #     '/diary/diary/'
    #     #     )
    #     data = [{
    #         "id": self.diary.id,
    #         "head": "test дневник",
    #         "content": "test описание дневника",
    #         "owner": self.user.pk,
    #     }]
    #     print(data)
    #     print(response)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #     # self.assertEqual(
    #     #     response,
    #     #     data
    #     # )

    # def test_update_diary(self):
    #     """
    #     Тест обновления дневника.
    #     """
    #     url = reverse("diary:diary-detail", args=(self.diary.pk,))
    #
    #     data = {
    #         "diary": "test дневник",
    #         "content": "test описание дневника, изменено"
    #     }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #     self.assertEqual(
    #         response.json()["diary"],
    #         "test описание дневника, изменено",
    #     )
    #
    # def test_create_entries(self):
    #     """
    #     Тест создания записи.
    #     """
    #     url = reverse("diary:entries-list")
    #     data = {
    #         "head": "test запись",
    #         "content": "test содержимое записи",
    #         "owner": self.user,
    #         "diary": self.diary,
    #         "publication_status": True
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_201_CREATED
    #     )
    #     self.assertEqual(
    #         Diary.objects.count(),
    #         1)
    #
    # def test_retrieve_entries(self):
    #     """
    #     Получение конкретной привычки.
    #     """
    #     url = reverse("diary:entries-detail", kwargs={"pk": self.entries.pk})
    #     response = self.client.get(url)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #     self.assertEqual(
    #         response.json()["entries"],
    #         "test запись"
    #     )
    #
    # def test_update_entries(self):
    #     """
    #     Тест на изменения привычки.
    #     """
    #     url = reverse("diary:entries-detail", args=(self.entries.pk,))
    #     data = {
    #         "head": "test запись",
    #         "content": "test содержимое записи, изменение"
    #     }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #     self.assertEqual(
    #         response.json()["entries"],
    #         "test запись",
    #     )
    #
    # def test_delete_entries(self):
    #     """
    #     Удаление привычки.
    #     """
    #     url = reverse("diary:entries-detail", args=(self.entries.pk,))
    #     response = self.client.delete(url)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_204_NO_CONTENT
    #     )
    #     self.assertEqual(Diary.objects.count(), 0)
    #
    # def test_delete_diary(self):
    #     """
    #     Удаление дневника.
    #     """
    #     url = reverse("diary:diary-detail", args=(self.diary.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_204_NO_CONTENT
    #     )
    #     self.assertEqual(Diary.objects.count(), 0)
