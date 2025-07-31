from rest_framework.serializers import ModelSerializer
from .models import Accommodation, City


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ["name"]


class AccommodationListSerializer(ModelSerializer):

    city = CitySerializer(read_only=True)

    class Meta:
        model = Accommodation
        fields = ["name", "type", "location", "city", "description"]
