from rest_framework.serializers import ModelSerializer, StringRelatedField
from packages.models import Package
from .models import Package, PackageDailyAvailability


class PackageDailyAvailabilitySerializer(ModelSerializer):
    """Serializer for displaying daily availability and price for a package"""

    class Meta:
        model = PackageDailyAvailability
        fields = ["date", "price", "status"]


class PackageSerializer(ModelSerializer):
    """Basic package serializer with daily availability data"""

    daily_prices = PackageDailyAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ["id", "name", "description", "price", "is_active", "daily_prices"]


class FilteredPackageSerializer(ModelSerializer):
    """Serializer for available package combinations with daily prices"""

    room_type = StringRelatedField()
    daily_prices = PackageDailyAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ["id", "name", "room_type", "description", "daily_prices"]
