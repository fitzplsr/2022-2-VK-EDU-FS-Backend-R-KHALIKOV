from django.urls import path
from .views import user_chats, user_messages

urlpatterns = [
    #path('', menu, name='menu'),
    path('chats_list/', user_chats, name='user_chats'),
    path('message/', user_messages, name='user_messages'),
]