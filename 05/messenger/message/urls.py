from django.urls import path
from .views import new_message, message_detail, message_edit, message_delete

urlpatterns = [
    path('new', new_message, name='mew_message'),
    path('', message_detail, name='message_detail'),
    path('edit', message_edit, name='message_edit'),
    path('delete/', message_delete, name='message_delete'),
]