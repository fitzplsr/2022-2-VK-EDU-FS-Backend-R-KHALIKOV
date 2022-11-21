from django.db import models
from django.utils import timezone
from users.models import User

class Chat(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Название чата',
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Описание чата',
        blank=True,
        null=True,
    )
    creating_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания чата'
    )
    editing_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования чата'
    )

    users = models.ManyToManyField(
        User,
        verbose_name='Участники чата',
        blank=True,
        related_name='chats'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'



