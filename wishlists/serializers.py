from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from accommodations.serializers import AccommodationListSerializer
from .models import Wishlist


class WishlistDetailSerializer(ModelSerializer):
    """Serializer for displaying detailed representation of a Wishlist"""

    accommodations = AccommodationListSerializer(many=True, read_only=True)
    username = CharField(source="user.username", read_only=True)
    name = CharField(required=True)

    def validate(self, data):

        # Throws an error if the required field is missing
        if "name" not in data:
            raise ValidationError({"name": "This field is required"})

        return data

    class Meta:
        model = Wishlist
        fields = ["name", "username", "accommodations"]
        read_only_fields = ["username", "accommodations"]
