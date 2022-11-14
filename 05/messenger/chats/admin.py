from django.contrib import admin
from .models import Chat
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Chat, ChatAdmin)
