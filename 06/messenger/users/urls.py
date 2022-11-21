from django.urls import path
from .views import user_chats, user_messages, user_info

urlpatterns = [
    path('chats_list/', user_chats, name='user_chats'),
    path('message/', user_messages, name='user_messages'),
    path('info/', user_info, name='user_info')
]