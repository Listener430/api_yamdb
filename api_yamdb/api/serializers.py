from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    User,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)

        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(), fields=("name", "slug")
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializerWriteOnly(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), many=False
    )

    def validate_year(self, value):
        current_year = timezone.now().year
        if not value <= current_year:
            raise serializers.ValidationError(
                "год должен быть не больше текущего",
            )
        return value

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class TitleSerializerReadOnly(serializers.ModelSerializer):
    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )
        read_only_fields = ("id", "author", "pub_date")
        model = Review

    def validate(self, data):
        if self.context["view"].action != "create":
            return data
        title_id = self.context["view"].kwargs.get("title_id")
        user = self.context["request"].user
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError("Нельзя оставить ревью дважды")
        return data

    def validate_year(self, value):
        if 1 < value < 10:
            raise serializers.ValidationError("Оценка не может быть более 10 и менее 1")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "pk",
            "first_name",
            "last_name",
            "email",
            "role",
            "bio",
        )
        model = User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
