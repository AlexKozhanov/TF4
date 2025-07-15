from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Класс Пользователи
    """
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email')
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        **NULLABLE)
    country = models.CharField(
        max_length=50,
        verbose_name='Страна',
        **NULLABLE)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
