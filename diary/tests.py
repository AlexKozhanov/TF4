from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from diary.models import Diary
from users.models import User


class DiaryTest(APITestCase):
    """
    Тестирование модели Diary.
    CRUD дневника.
    """

    def setUp(self):
        """
        Создание данных перед тестированием.
        """
        self.user = User.objects.create(email="test@test.ru")
        users_group = Group.objects.get(name='Пользователи')
        self.user.groups.add(users_group)
        self.diary = Diary.objects.create(
            head="test дневник",
            content="test описание дневника",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_diary(self):
        """
        Тест вывод всех дневников.
        """
        url = reverse("diary:diary-list")
        response = self.client.get(url)

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.diary.id,
                    "head": "test дневник",
                    "content": "test описание дневника",
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            result
        )

    def test_update_diary(self):
        """
        Тест обновления дневника.
        """
        url = reverse("diary:diary-detail", args=(self.diary.pk,))

        data = {
            "diary": "test дневник",
            "content": "test описание дневника, изменено"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["diary"],
            "test описание дневника, изменено",
        )

    def test_create_entries(self):
        """
        Тест создания записи.
        """
        url = reverse("diary:entries-list")
        data = {
            "head": "test запись",
            "content": "test содержимое записи",
            "owner": self.user,
            "diary": self.diary,
            "publication_status": True
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Diary.objects.count(),
            1)

    def test_retrieve_entries(self):
        """
        Получение конкретной привычки.
        """
        url = reverse("diary:entries-detail", kwargs={"pk": self.entries.pk})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["entries"],
            "test запись"
        )

    def test_update_entries(self):
        """
        Тест на изменения привычки.
        """
        url = reverse("diary:entries-detail", args=(self.entries.pk,))
        data = {
            "head": "test запись",
            "content": "test содержимое записи, изменение"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["entries"],
            "test запись",
        )

    def test_delete_entries(self):
        """
        Удаление привычки.
        """
        url = reverse("diary:entries-detail", args=(self.entries.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Diary.objects.count(), 0)

    def test_delete_diary(self):
        """
        Удаление дневника.
        """
        url = reverse("diary:diary-detail", args=(self.diary.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Diary.objects.count(), 0)
