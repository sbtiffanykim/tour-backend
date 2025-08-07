from rest_framework.serializers import ModelSerializer, CharField
from accommodations.serializers import AccommodationListSerializer
from .models import Wishlist


class WishlistDetailSerializer(ModelSerializer):
    """Serializer for displaying detailed representation of a Wishlist"""

    accommodations = AccommodationListSerializer(many=True)
    username = CharField(source="user.username")

    class Meta:
        model = Wishlist
        fields = ["name", "username", "accommodations"]
        read_only_fields = ["username"]
