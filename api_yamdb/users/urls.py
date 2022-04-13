from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import TokenObtainPairView, UserViewSet, get_confirmation_code

router_v1 = DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path(
        "v1/auth/email/",
        get_confirmation_code,
        name="get_confirmation_code",
    ),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
