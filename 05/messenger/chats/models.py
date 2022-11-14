from django.db import models
from django.utils import timezone
from users.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, verbose_name='Участники чата', blank=True, related_name='chats')

    def __str__(self):
        return f'Chat_id:{self.pk}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'



