from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .mixins import PhoneNumberValidationMixin

User = get_user_model()


class SignUpSeriailzer(PhoneNumberValidationMixin, serializers.ModelSerializer):
    """Seraizlier for user registration. Includes custom validation for password strength and phone number format"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
