from django.urls import path, include
from .views import menu, show_chats, new_chat, chat_detail, delete_user, add_user

urlpatterns = [
    path('', menu, name='menu'),
    path('chats_list/', show_chats, name='show_chats'),
    path('chats_list/dialog/', chat_detail, name='chat_detail'),
    path('chats_list/dialog/delete_user/', delete_user, name='delete_user'),
    path('chats_list/dialog/add_user/', add_user, name='add_user'),
    path('chats_list/dialog/message/', include('message.urls')),
    path('chats_list/dialog/new/', new_chat, name='new_chat')
]