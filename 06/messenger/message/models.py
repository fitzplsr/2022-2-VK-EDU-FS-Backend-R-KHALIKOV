from django.db import models
from chats.models import Chat
from users.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name='Отправитель'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name='Чат'
    )
    creating_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Время отправки',
    )
    editing_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Время редактирования'
    )
    content = models.CharField(
        max_length=255,
        verbose_name='Содержание'
    )
    is_editing = models.BooleanField(
        default=False,
        verbose_name='Отредактировано'
    )
    is_reading = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )

    def __str__(self):
        return f'Отправитель:{self.sender}, Время отправления:{self.creating_time}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'