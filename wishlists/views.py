from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Wishlist
from .serializers import WishlistDetailSerializer


def get_wishlist_or_404(pk, user):
    """A function to retrieve a wishlist. Throws 404 error if a wishlist does not exist"""
    try:
        wishlist = Wishlist.objects.get(pk=pk)
        if user != wishlist.user:
            raise PermissionDenied({"error": "You do not have a permission to access this wishlist"})
    except Wishlist.DoesNotExist:
        raise NotFound({"error": "Wishlist not found"})
    return wishlist


class WishlistDetailView(APIView):
    """API view that allows an authenticated user to retrieve or delete or update(name only) their own wishlist"""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        wishlist = get_wishlist_or_404(pk, request.user)
        serializer = WishlistDetailSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        wishlist = get_wishlist_or_404(pk, request.user)
        serializer = WishlistDetailSerializer(wishlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        wishlist = get_wishlist_or_404(pk, request.user)
        wishlist.delete()
        return Response({"message": "Your wishlist deleted"}, status=status.HTTP_204_NO_CONTENT)


class CreateWishlistView(APIView):
    """API view that allows an authenticated user to create their own wishlist"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # if a user already have their own wishlist, returns an error
        if hasattr(request.user, "wishlists"):
            return Response({"error": "You already have a wishlist"}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get("name", f"{request.user}'s wishlist")
        wishlist = Wishlist.objects.create(name=name, user=request.user)
        serializer = WishlistDetailSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
