from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserCustomAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'branch')
    fieldsets = (
        ("Auth", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "branch")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, UserCustomAdmin)
