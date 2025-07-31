from django.contrib.auth import authenticate, logout, login
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSeriailzer, PrivateUserSerializer, ChangePasswordSerializer


class SignUpView(APIView):

    def post(self, request):
        serializer = SignUpSeriailzer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "user": {
                        "username": serializer.data["username"],
                        "first_name": serializer.data["first_name"],
                        "last_name": serializer.data["last_name"],
                        "email": serializer.data["email"],
                        "phone_number": serializer.data["phone_number"],
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


class LogInView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ValidationError("Username and password are required")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": "Login successfully"}, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Invalid username or password")


class PrivateUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PrivateUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = PrivateUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_profile = serializer.save()
        return Response(PrivateUserSerializer(validated_profile).data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)
