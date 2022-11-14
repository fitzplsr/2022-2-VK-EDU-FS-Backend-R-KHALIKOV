# Generated by Django 3.2.12 on 2022-11-13 22:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0004_alter_message_creating_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Участники чата'),
        ),
    ]