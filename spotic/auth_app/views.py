from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import RegisterSerializer, ProfileSerializer, LoginSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        user = RegisterSerializer(data=request.data)
        if user.is_valid():
            user = user.save()
            refresh = RefreshToken.for_user(user)  # type: ignore
            return Response(
                {
                    "user": ProfileSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]  # type: ignore
            refresh = RefreshToken.for_user(user)  # type: ignore
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # type: ignore
