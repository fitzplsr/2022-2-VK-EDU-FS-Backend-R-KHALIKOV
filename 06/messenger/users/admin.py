from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'username')
    list_filter = ('is_active',)


admin.site.register(User, UserAdmin)
