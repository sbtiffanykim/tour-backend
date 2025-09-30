from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, BookingStatusChoices
from .serializers import BookingDetailSerializer


def get_booking_for_user_or_guest(request, booking_id):
    """Retrieve a booking for authenticated users or guest with phone verification"""
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        raise NotFound("Booking not found.")

    # Logged-in user: can only access their own bookings
    if request.user.is_authenticated:
        if request.user != booking.user:
            raise PermissionDenied("You do not have permission to view this booking.")
        return booking

    # Guest access: must provide phone number
    guest_phone = request.query_params.get("phone")
    if not guest_phone or not booking.guest_user or guest_phone != booking.guest_user.phone_number:
        raise PermissionDenied("Invalid guest credentials")
    return booking


class BookingDetailView(generics.RetrieveAPIView):
    """Retrieve a single booking (both logged-in and guest users)"""

    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    permission_classes = []  # allow both logged-in and guest users

    def get_object(self):
        return get_booking_for_user_or_guest(self.request, self.kwargs["pk"])


class BookingCancelRequestView(APIView):
    """Enables to cancel own booking (both loggged-in and guest users)"""

    permission_classes = []  # allow both logged-in and guest users

    def post(self, request, pk):
        booking = get_booking_for_user_or_guest(request, pk)

        if booking.status == BookingStatusChoices.CANCEL_REQUESTED:
            return Response({"detail": "Already requested cancellation."}, status=status.HTTP_400_BAD_REQUEST)

        # Change status
        booking.status = BookingStatusChoices.CANCEL_REQUESTED
        booking.save()

        return Response({"detail": "Cancellation requested."}, status=status.HTTP_200_OK)
