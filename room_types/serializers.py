from rest_framework.serializers import ModelSerializer
from .models import RoomType
from packages.serializers import PackageSerializer


class RoomTypeWithPackageSerializer(ModelSerializer):

    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = RoomType
        fields = "__all__"
