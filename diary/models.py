from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Diary(models.Model):
    """
    Класс-модель Личный Дневник
    """
    head = models.CharField(
        max_length=100,
        verbose_name='Заголовок')
    content = models.TextField(
        max_length=255,
        **NULLABLE,
        verbose_name='Содержимое дневника')
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        **NULLABLE,
        verbose_name='Владелец')

    class Meta:
        verbose_name = 'Дневник'
        verbose_name_plural = 'Дневники'
        ordering = ['head', 'content', 'owner']

    def __str__(self):
        return self.head


class DiaryEntries(models.Model):
    """
    Класс-модель Записи в Дневнике
    """
    head = models.CharField(
        max_length=100,
        verbose_name='Заголовок')
    content = models.TextField(
        max_length=2000,
        **NULLABLE,
        verbose_name='Содержимое')
    owner_entries = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        **NULLABLE,
        verbose_name='Владелец')
    diary = models.ForeignKey(
        Diary,
        # on_delete=models.CASCADE,
        on_delete=models.SET_NULL,
        default=None,
        verbose_name='Дневник',
        **NULLABLE,
        help_text='Выберите название Дневника, в котором будет лежать эта запись')
    publication_status = models.BooleanField(
        verbose_name='Статус публикации',
        default=False,
        **NULLABLE,
        help_text='Публиковать на первую страницу?')
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0)
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Записи в дневнике'
        verbose_name_plural = 'Записи в дневникае'
        ordering = ['head', 'content', 'owner_entries', 'diary', 'publication_status']

    def __str__(self):
        return self.head
