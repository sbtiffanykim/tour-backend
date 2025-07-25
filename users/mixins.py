import re
from rest_framework.serializers import ValidationError


class PhoneNumberValidationMixin:
    def validate_phone_number(self, value):
        phone_regex = r"^01[0-9]{8,9}$"
        # Validate the phone number format to prevent SQL injection
        if not re.match(phone_regex, value):
            raise ValidationError("Phone number should be in digits")
        return value
