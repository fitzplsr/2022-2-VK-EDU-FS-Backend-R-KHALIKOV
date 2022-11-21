from django.urls import path
from .views import new_message, message_detail, edit_message, delete_message, read_message

urlpatterns = [
    path('new', new_message, name='mew_message'),
    path('', message_detail, name='message_detail'),
    path('edit', edit_message, name='edit_message'),
    path('delete/', delete_message, name='delete_message'),
    path('read/', read_message, name='read_message'),
]