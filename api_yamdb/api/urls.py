from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="Reviewqrst",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="Commentqrst",
)

urlpatterns = [
    path("v1/", include(router.urls), name="api_urls"),
]
