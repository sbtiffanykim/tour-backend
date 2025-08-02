from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch
from datetime import datetime, date, timedelta
from .models import Accommodation
from room_types.models import RoomType
from packages.models import Package, PackagePrice
from .serializers import AccommodationListSerializer, AccommodationDetailSerializer, AllPackageCombinationsSerializer
from users.models import User


class AccommodationListView(ListAPIView):
    """API view to retrieve a list of accommodations"""

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
    """API view to retrieve an accommodation detailed info"""

    def get(self, request, pk):
        try:
            accommodation = Accommodation.objects.get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found")
        serializer = AccommodationDetailSerializer(accommodation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllPackageCombinationsView(APIView):
    """Returns all room_type + package combinations for a given accommodation regardless of availability or selected date"""

    def get(self, request, pk):

        if not Accommodation.objects.get(pk=pk).exists():
            raise NotFound("Accommodation not found")
        combinations = RoomType.objects.filter(accommodation_id=pk).prefetch_related(
            Prefetch("packages", queryset=Package.objects.filter(is_active=True))
        )
        serializer = AllPackageCombinationsSerializer(combinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
