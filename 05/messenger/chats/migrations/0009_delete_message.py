# Generated by Django 3.2.12 on 2022-11-14 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_alter_message_chat'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
