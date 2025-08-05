from rest_framework.serializers import ModelSerializer
from .models import Package, PackageDailyAvailability


class PackageDailyAvailabilitySerializer(ModelSerializer):

    class Meta:
        model = PackageDailyAvailability
        fields = ["date", "price", "status"]


class PackageSerializer(ModelSerializer):

    daily_prices = PackageDailyAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ["id", "name", "description", "price", "is_active", "daily_prices"]
