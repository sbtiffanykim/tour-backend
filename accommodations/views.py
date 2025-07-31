from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Accommodation
from .serializers import AccommodationListSerializer, AccommodationDetailSerializer
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
    """API view to retreive an accommodation with given info"""

    def get_object(self, pk):
        try:
            # media(photos) should be added after implementing a media model
            return Accommodation.objects.prefetch_related("room_types__packages").get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found")

    def get(self, request, pk):
        accommodation = self.get_object(pk)
        serializer = AccommodationDetailSerializer(accommodation)
        return Response(serializer.data, status=status.HTTP_200_OK)
