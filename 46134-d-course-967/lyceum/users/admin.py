from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import User

import users.models

__all__ = []


class ProfileInline(admin.TabularInline):
    model = users.models.Profile
    readonly_fields = ("birthday", "image", "coffee_count")
    can_delete = False


class UserAdmin(BaseAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
