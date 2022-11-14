from django.db import models
from chats.models import Chat
from users.models import User
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message', verbose_name='Отправитель')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message', verbose_name='Чат')
    creating_time = models.DateTimeField(editable=False, verbose_name='Время отправки')
    content = models.CharField(max_length=255, verbose_name='Содержание')

    def __str__(self):
        return f'Отправитель:{self.sender}, Содержание:{self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'