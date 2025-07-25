import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSeriailzer(serializers.ModelSerializer):
    """Seraizlier for user registration. Includes custom validation for password strength and phone number format"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password"]

    def validate_password(self, value):
        # Validate user's password length
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        # Ensure password includes both letters and numbers
        if not re.search(r"\d", value) or not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("Password must contain both letters and numbers")
        return value

    def validate_phone_number(self, value):
        # Validate the phone number format to prevent SQL injection
        if not value.isdigit():
            raise serializers.ValidationError("Phone number should be in digits")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
