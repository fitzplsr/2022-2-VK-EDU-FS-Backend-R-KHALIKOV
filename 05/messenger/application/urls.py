from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/', include('chats.urls')),
    path('users/', include('users.urls')),
    #path('', include('chat_settings.urls')),
]
