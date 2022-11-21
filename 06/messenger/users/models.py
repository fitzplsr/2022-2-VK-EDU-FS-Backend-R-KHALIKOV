from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        blank=True
    )
    nickname = models.CharField(
        null=True,
        max_length=10,
        blank=True,
        verbose_name='Псевдоним'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='День рождения'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
