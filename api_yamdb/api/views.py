from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .filters import TitleFilter
from .mixins import CreateDestroyListMixin
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminRole,
    IsAdminModerator,
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
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


class CategoryViewSet(CreateDestroyListMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "slug")
    lookup_field = "slug"


class GenreViewSet(CreateDestroyListMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("slug", "name")
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializerReadOnly
        return TitleSerializerWriteOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModerator,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id"),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            author=self.request.user,
            title=title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModerator,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        queryset = review.comments.all()
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
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if request.user.is_admin or request.user.is_moderator:
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=User.RoleChoices.USER)
        return Response(serializer.data, status=status.HTTP_200_OK)
