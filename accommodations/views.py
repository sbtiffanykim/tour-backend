from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch
from datetime import datetime, timedelta

from .models import Accommodation
from room_types.models import RoomType
from packages.models import Package, PackageDailyAvailability, AvailabilityStatus
from .serializers import (
    AccommodationListSerializer,
    AccommodationDetailSerializer,
    AllRoomPackagesSerializer,
    FilteredPackageSerializer,
)


def validate_dates(check_in_str, check_out_str):
    """Validate check_in and check_out dates"""
    if not check_in_str and not check_out_str:
        today = timezone.now().date()
        return today, today + timedelta(days=1)

    if (check_in_str and not check_out_str) or (not check_in_str and check_out_str):
        raise ValidationError({"error": "Both 'check_in' and 'check_out' must be provided together"})

    try:
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError({"error": "Invalid date format. Use 'YYYY-MM-DD'"})

    if check_in >= check_out:
        raise ValidationError({"error": "'check_in' must be earlier than 'check_out'"})

    return check_in, check_out


class AccommodationListView(ListAPIView):
    """API view to retrieve a list of accommodations with optional region filter"""

    serializer_class = AccommodationListSerializer

    def get_queryset(self):
        region = self.request.query_params.get("region")
        queryset = Accommodation.objects.all()
        if region:
            queryset = queryset.filter(region=region)
        return queryset

    def list(self, request, *args, **kwargs):
        accommodations = self.get_queryset()
        region = self.request.query_params.get("region", "all")
        if not accommodations.exists():
            return Response({"error": "No accommodations found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(accommodations, many=True)
        return Response({"region": region, "data": serializer.data}, status=status.HTTP_200_OK)


class AccommodationDetailView(APIView):
    """API view to retrieve detailed info about a specific accommodation"""

    def get(self, request, pk):
        try:
            accommodation = Accommodation.objects.get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found")
        serializer = AccommodationDetailSerializer(accommodation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomPackageListView(APIView):
    """API view to retrieve all room types and package combinations for a given accommodation"""

    def get(self, request, pk):

        if not Accommodation.objects.filter(pk=pk).exists():
            raise NotFound("Accommodation not found")
        room_types = RoomType.objects.filter(accommodation_id=pk).prefetch_related(
            Prefetch("packages", queryset=Package.objects.filter(is_active=True))
        )
        serializer = AllRoomPackagesSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailableRoomPackagesView(APIView):
    """API view to retrieve filtered available room-package combinations based on user selection"""

    def get(self, request, pk):

        # Parse query parameters
        check_in_str = request.query_params.get("check_in")
        check_out_str = request.query_params.get("check_out")
        guests = int(request.query_params.get("guests", 2))

        # Validate dates
        check_in, check_out = validate_dates(check_in_str, check_out_str)

        # Fetching data with given conditions
        packages = Package.objects.filter(
            is_active=True,
            room_type__accommodation_id=pk,
            room_type__base_occupancy__lte=guests,
            room_type__max_occupancy__gte=guests,
        ).prefetch_related(
            Prefetch(
                "daily_prices",
                queryset=PackageDailyAvailability.objects.filter(
                    status=AvailabilityStatus.OPEN, date__gte=check_in, date__lt=check_out
                ),
            )
        )
        # Filter out packages without daily_prices or room_type
        available_packages = [pkg for pkg in packages if pkg.room_type and pkg.daily_prices.all()]

        serializer = FilteredPackageSerializer(available_packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
