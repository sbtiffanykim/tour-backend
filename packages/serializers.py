from rest_framework.serializers import ModelSerializer
from .models import Package, PackageDailyAvailability


class PackageDailyAvailabilitySerializer(ModelSerializer):
    """Daily availability and price for a package"""

    class Meta:
        model = PackageDailyAvailability
        fields = ["date", "price", "status"]


class PackageSerializer(ModelSerializer):
    """Basic package serializer with daily availability data"""

    daily_prices = PackageDailyAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ["id", "name", "description", "price", "is_active", "daily_prices"]
