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


class PrivateUserSerializer(PhoneNumberValidationMixin, serializers.ModelSerializer):
    """Serializer for retrieving the authenticated user's profile information."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "avatar", "points"]
        read_only_fields = ["username", "points"]  # normal user cannot change points and his username

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password. Includes custom validation to ensure passwords match."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect")
        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords do not match")

        validate_password(new_password)
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
