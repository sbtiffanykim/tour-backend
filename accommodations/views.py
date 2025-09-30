from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Accommodation
from .serializers import AccommodationListSerializer, AccommodationDetailSerializer, CreateAccommodationSerializer


class AccommodationCollectionView(APIView):
    """
    GET: List all accommodations
    POST: Create accommodation with default values for missing fields
    """

    def get(self, request):
        region = request.query_params.get("region", "all")
        accommodations = Accommodation.objects.all()
        print(accommodations)

        if not accommodations.exists():
            return NotFound("Accommodation not found.")

        if region != "all":
            accommodations = accommodations.filter(region=region)

        serializer = AccommodationListSerializer(accommodations, many=True)
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
