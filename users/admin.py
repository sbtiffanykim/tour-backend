from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ["username", "is_staff", "is_superuser"]
    list_filter = ["is_staff", "is_superuser"]

    fieldsets = (
        (("Personal info"), {"fields": ["username", "email", "first_name", "last_name", "phone_number"]}),
        (
            ("Permissions"),
            {
                "fields": ["is_active", "is_staff", "is_superuser"],
                "classes": ["collapse"],
            },
        ),
        (("Additional info"), {"fields": ["avatar", "points", "last_login", "date_joined"], "classes": ["collapse"]}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "phone_number", "first_name", "last_name"],
            },
        ),
    )

    search_fields = ["username", "phone_number"]
    ordering = ["username"]
