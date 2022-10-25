from django.db import models


class Chat(models.Model):
    users = models.ManyToManyField('User')


class User(models.Model):
    name = models.CharField(max_length=30)


class Message(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    create_time = models.TimeField()
    content = models.CharField(max_length=255)