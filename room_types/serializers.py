from rest_framework.serializers import ModelSerializer, ValidationError
from .models import RoomType


class RoomTypeCollectionSerializer(ModelSerializer):
    """Serializer for creating/displaying room types"""

    class Meta:
        model = RoomType
        fields = "__all__"
        extra_kwargs = {"accommodation": {"required": False}}

    def create(self, validated_data):
        accommodation_id = self.context.get("accommodation_id")
        if not accommodation_id:
            raise ValidationError({"accommodation_id": "Accommodation pk is required."})

        if not validated_data.get("name"):
            raise ValidationError({"name": "This field is required."})

        validated_data["accommodation_id"] = accommodation_id
        return super().create(validated_data)
