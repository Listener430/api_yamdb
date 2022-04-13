from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL

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
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data["username"]
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data["confirmation_code"]
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_user(user)
    return Response({"token": str(token.access_token)}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def code(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data["username"]
        email = serializer.data["email"]
        user = get_object_or_404(User, username=username, email=email)
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения"
    message = f"{confirmation_code} - код для авторизации"
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
