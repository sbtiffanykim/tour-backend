from rest_framework.serializers import ModelSerializer
from .models import Package, PackagePrice


class PackagePriceSerializer(ModelSerializer):

    class Meta:
        model = PackagePrice
        fields = ["date", "price", "status"]


class PackageSerializer(ModelSerializer):

    daily_prices = PackagePriceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = "__all__"
