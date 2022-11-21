# Generated by Django 3.2.12 on 2022-11-20 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chats', '0005_chat_editing_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creating_time', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')),
                ('editing_time', models.DateTimeField(auto_now=True, verbose_name='Время редактирования')),
                ('content', models.CharField(max_length=255, verbose_name='Содержание')),
                ('is_editing', models.BooleanField(default=False, verbose_name='Отредактировано')),
                ('is_reading', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='chats.chat', verbose_name='Чат')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]