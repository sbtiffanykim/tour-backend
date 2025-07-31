from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Accommodation
from .serializers import AccommodationListSerializer


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
        if not accommodations.exists():
            return Response({"error": "No accommodations found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(accommodations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
