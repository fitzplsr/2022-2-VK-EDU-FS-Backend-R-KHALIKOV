from django.contrib import admin
from .models import Message
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'creating_time', 'content',)
    list_filter = ('creating_time',)


admin.site.register(Message, MessageAdmin)