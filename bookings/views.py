from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, BookingStatusChoices
from .serializers import BookingDetailSerializer


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    permission_classes = []  # allow both logged-in and guest users

    def get_object(self):
        booking = super().get_object()

        # 1. If the user is logged in, only allow their own bookings
        if self.request.user.is_authenticated:
            if self.request.user != booking.user:
                raise PermissionDenied("You do not have permission to view this booking.")
            return booking

        # 2. Guest user access with booking id + phone verification
        guest_phone = self.request.query_params.get("phone")

        if not booking.guest_user:
            raise PermissionDenied()
        if guest_phone and guest_phone == booking.guest_user.phone_number:
            return booking

        raise PermissionDenied("Invalid guest credentials")
