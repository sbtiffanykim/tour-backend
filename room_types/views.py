from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from .serializers import RoomTypeCollectionSerializer
from accommodations.models import Accommodation


class RoomTypeCollectionView(APIView):
    """
    GET: List all room types of an accommodations
    POST: Create a room type
    """

    def get(self, request, pk):
        try:
            room_types = Accommodation.objects.get(pk=pk).room_types.all()
        except:
            raise NotFound("Room type not found")
        serializer = RoomTypeCollectionSerializer(room_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = RoomTypeCollectionSerializer(data=request.data, context={"accommodation_id": pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
