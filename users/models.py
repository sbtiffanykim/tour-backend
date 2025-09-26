from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator


class CustomBaseUser(models.Model):
    """Abstract base model for all users(registered or non-registered). Stores common information."""

    phone_validator = RegexValidator(regex=r"^01[0-9]{8,9}$", message="The phone number format is invalid")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator],
        error_messages={
            "unique": ("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(max_length=15, validators=[phone_validator])

    class Meta:
        abstract = True


class User(AbstractUser, CustomBaseUser):
    """Custom user model for registered users."""

    avatar = models.ImageField(null=True, blank=True)
    points = models.PositiveIntegerField(default=0)


class GuestInfo(CustomBaseUser):
    """Stores guest information for non-register bookings."""

    def __str__(self):
        return f"Guest: {self.first_name} {self.last_name}_{self.phone_number}"
