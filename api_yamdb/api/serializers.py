from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Sum

from reviews.models import (
    Category,
    Genre,
    Title,
    GenresTitle,
    Review,
    Comment,
    User,
)
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")

    validators = [
        UniqueTogetherValidator(
            queryset=Category.objects.all(), fields=("name", "slug")
        )
    ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

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

    def get_rating(self, obj):
        if Review.objects.filter(title_id=obj.id).exists():
            rating = (
                Review.objects.filter(title_id=obj.id).aggregate(
                    sum=Sum("score")
                )["sum"]
                or 0
            ) / Review.objects.filter(title_id=obj.id).count()
        else:
            rating = 0

        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        title_id = self.context["view"].kwargs["title_id"]
        author = self.context["request"].user
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError("Нельзя оставить ревью дважды")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

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
