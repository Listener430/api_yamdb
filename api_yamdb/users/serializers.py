from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ConfirmationCode, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]
        model = User


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False

    def validate(self, attrs):
        password = self.context["request"].data.get("confirmation_code")
        attrs["password"] = password
        return super().validate(attrs)


class ConfirmationCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.SlugRelatedField(
        slug_field="confirmation_code", many=False, read_only=True
    )
    email = serializers.SlugRelatedField(slug_field="email", many=False, read_only=True)
    code_date = serializers.DateTimeField()

    class Meta:
        fields = "__all__"
        model = ConfirmationCode
