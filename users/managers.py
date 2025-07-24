from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Creates and saves user with the required fields: username, email, first_name, last_name, phone_number, password"""

    # Create a user with the given fields
    def create_user(self, username, email, first_name, last_name, phone_number, password, **extra_fields):
        required_fields = {
            "Username": username,
            "Email": email,
            "First name": first_name,
            "Last name": last_name,
            "Phone Number": phone_number,
            "Password": password,
        }

        for field, value in required_fields.items():
            if not value:
                raise ValueError(f"{field} is required")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, first_name, last_name, phone_number, password, **extra_fields)
