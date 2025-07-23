from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    phone_validator = RegexValidator(regex=r"^01[0-9]-\d{3,4}-\d{4}$", message="The phone number format is invalid")

    avatar = models.ImageField()
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    points = models.PositiveIntegerField(default=0)
