from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "phone_number", "is_staff"]


@admin.register(User)
class UserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

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
                "fields": [
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ],
            },
        ),
    )

    search_fields = ["username", "phone_number"]
    ordering = ["username"]
