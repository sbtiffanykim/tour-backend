from rest_framework.serializers import ModelSerializer
from .models import Accommodation, City, Amenity
from room_types.models import RoomType
from room_types.serializers import RoomTypeWithPackageSerializer


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ["name"]


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = ["name", "description"]


class AccommodationListSerializer(ModelSerializer):

    city = CitySerializer(read_only=True)

    class Meta:
        model = Accommodation
        fields = ["name", "type", "location", "city", "description"]


class AccommodationDetailSerializer(ModelSerializer):

    amenities = AmenitySerializer(read_only=True, many=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Accommodation
        fields = "__all__"


class AllPackageCombinationsSerializer(ModelSerializer):

    class Meta:
        model = RoomType
        exclude = ["accommodation"]
