from django.contrib import admin
from .models import Message
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'creating_time', 'content', 'editing_time', 'is_editing', 'is_reading',)
    list_filter = ('creating_time',)


admin.site.register(Message, MessageAdmin)