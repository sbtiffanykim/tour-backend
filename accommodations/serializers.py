from rest_framework.serializers import ModelSerializer
from .models import Accommodation, City, Amenity, AccommodationType
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


class CreateAccommodationSerializer(ModelSerializer):
    """Serializer for creating a new accommodation"""

    class Meta:
        model = Accommodation
        fields = "__all__"

    # def create(self, validated_data):
    #     # optioanl fields: put a default value if user does not sends
    #     validated_data.setdefault("type", AccommodationType.RESORT)
    #     validated_data.setdefault("x_coordinate", 0)
    #     validated_data.setdefault("y_coordinate", 0)
    #     validated_data.setdefault("homepage", "")
    #     validated_data.setdefault("description", "")
    #     validated_data.setdefault("check_in", None)
    #     validated_data.setdefault("check_out", None)
    #     validated_data.setdefault("cancellation_policy", None)
    #     validated_data.setdefault("info", "")

    #     amenities_data = validated_data.pop("amenities", [])
    #     accommodation = super().create(validated_data)
    #     if amenities_data:
    #         accommodation.amenities.set(amenities_data)

    #     return accommodation


class AllRoomPackagesSerializer(ModelSerializer):
    """Serializer for retrieving all packages for a room type"""

    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = "__all__"
