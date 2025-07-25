from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSeriailzer


class SignUpView(APIView):

    def post(self, request):
        serializer = SignUpSeriailzer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "user": {
                        "Username": serializer.data["username"],
                        "First name": serializer.data["first_name"],
                        "Last name": serializer.data["last_name"],
                        "Email": serializer.data["email"],
                        "Phone number": serializer.data["phone_number"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"success": "Logout successfully"}, status=status.HTTP_200_OK)
