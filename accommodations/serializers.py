from rest_framework.serializers import ModelSerializer
from .models import Accommodation, City, Amenity
from room_types.models import RoomType
from packages.serializers import PackageSerializer


class CitySerializer(ModelSerializer):
    """Serializer for displaying city with its name only"""

    class Meta:
        model = City
        fields = ["name"]


class AmenitySerializer(ModelSerializer):
    """Serializer for displaying amenity details"""

    class Meta:
        model = Amenity
        fields = ["name", "description"]


class AccommodationListSerializer(ModelSerializer):
    """Serializer for listing accommodations with basic info"""

    city = CitySerializer(read_only=True)

    class Meta:
        model = Accommodation
        fields = ["name", "type", "location", "city", "description"]


class AccommodationDetailSerializer(ModelSerializer):
    """Serializer for detailed accommodation with its info"""

    amenities = AmenitySerializer(read_only=True, many=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Accommodation
        fields = "__all__"


class AllRoomPackagesSerializer(ModelSerializer):
    """Serializer for retrieving all packages for a room type"""

    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = "__all__"
