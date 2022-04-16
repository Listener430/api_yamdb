from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import send_confirmation_code
from .models import User
from .serializers import (
    UserSerializer,
    SignupSerializer,
    TokenSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data["confirmation_code"]
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_user(user)
    return Response({"token": str(token.access_token)}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def code(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    user = get_object_or_404(User, username=username, email=email)
    send_confirmation_code(user)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
