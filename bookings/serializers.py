from rest_framework.serializers import ModelSerializer

from .models import Booking
from users.serializers import PrivateUserSerializer


class BookingDetailSerializer(ModelSerializer):

    user = PrivateUserSerializer()

    class Meta:
        model = Booking
        fields = "__all__"
