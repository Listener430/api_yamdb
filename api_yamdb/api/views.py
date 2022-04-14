from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework


from .permissions import (
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAdminRole,
    IsAdminModerator,
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    User,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerReadOnly,
    TitleSerializerWriteOnly,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    AdminUserSerializer,
)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "slug")
    lookup_field = "slug"


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("slug", "name")
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ["year"]

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get("genre", None)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        category = self.request.query_params.get("category", None)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        name = self.request.query_params.get("name", None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializerReadOnly
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return TitleSerializerWriteOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs["title_id"]),
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs["review_id"]),
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminRole,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    lookup_value_regex = r"[\w\@\.\+\-]+"
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        url_name="me",
        permission_classes=(IsAuthenticated,),
    )
    def about_me(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if request.user.is_admin or request.user.is_moderator:
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role="user")
        return Response(serializer.data, status=status.HTTP_200_OK)
