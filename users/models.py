from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator


class User(AbstractUser):

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
    avatar = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    points = models.PositiveIntegerField(default=0)
