from rest_framework.serializers import ModelSerializer
from .models import Accommodation


class AccommodationListSerializer(ModelSerializer):

    class Meta:
        model = Accommodation
        fields = ["name", "location", "region", "description"]
