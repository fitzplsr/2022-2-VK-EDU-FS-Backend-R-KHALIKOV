from django.urls import path, include
from .views import menu, show_chats, new_chat, chat_detail, delete_user, add_user, delete_chat, edit_chat, chat_messages

urlpatterns = [
    path('', menu, name='menu'),
    path('chats_list/', show_chats, name='show_chats'),
    path('chats_list/chat/', chat_detail, name='chat_detail'),
    path('chats_list/chat/delete_user/', delete_user, name='delete_user'),
    path('chats_list/chat/add_user/', add_user, name='add_user'),
    path('chats_list/chat/message/', include('message.urls')),
    path('chats_list/chat/new', new_chat, name='new_chat'),
    path('chats_list/chat/delete/', delete_chat, name='delete_chat'),
    path('chats_list/chat/edit', edit_chat, name='edit_chat'),
    path('chats_list/chat/messages/', chat_messages, name='chat_messages')
]