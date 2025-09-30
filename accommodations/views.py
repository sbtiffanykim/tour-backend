from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Accommodation, Amenity
from .serializers import (
    AccommodationListSerializer,
    AccommodationDetailSerializer,
    CreateAccommodationSerializer,
    AmenitySerializer,
)


class AccommodationCollectionView(APIView):
    """
    GET: List all accommodations
    POST: Create accommodation with default values for missing fields
    """

    def get(self, request):
        region = request.query_params.get("region", "all")
        accommodations = Accommodation.objects.all()
        if not accommodations.exists():
            return NotFound("Accommodation not found.")
        if region != "all":
            accommodations = accommodations.filter(region=region)

        serializer = AccommodationListSerializer(accommodations, many=True)
        return Response({"region": region, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        required_fields = ["name", "location", "region"]
        missing_or_empty = [field for field in required_fields if not request.data.get(field)]
        if missing_or_empty:
            raise ValidationError({field: "This field is required." for field in missing_or_empty})

        serializer = CreateAccommodationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccommodationDetailView(APIView):
    """API view to retrieve detailed info about a specific accommodation"""

    def get(self, request, pk):
        try:
            accommodation = Accommodation.objects.get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found")
        serializer = AccommodationDetailSerializer(accommodation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AmenityCollectionView(APIView):
    """
    GET: List all amenities
    POST: Create amenity
    """

    def get(self, request):
        try:
            amenities = Amenity.objects.all()
        except Amenity.DoesNotExist:
            raise NotFound("Amenity not found")
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
