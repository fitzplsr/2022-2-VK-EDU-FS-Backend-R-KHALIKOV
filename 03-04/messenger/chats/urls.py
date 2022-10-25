from django.urls import path
from .views import menu, show_chats, new_chat, chat_detail

urlpatterns = [
    path('', menu, name='menu'),
    path('chats_list/', show_chats, name='show_chats'),
    path('chats_list/dialog/', chat_detail, name='chat_detail'),
    path('chats_list/new/', new_chat, name='new_chat')
]