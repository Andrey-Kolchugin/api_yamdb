from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'role', 'confirmation_code',)
    search_fields = ('email', 'username',) 
    list_filter = ('role',)
    list_editable = ('email', 'username', 'role', 'confirmation_code',)
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)