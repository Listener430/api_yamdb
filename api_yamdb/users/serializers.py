from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User
