from django.urls import include, path

from .views import code, signup, token


urlpatterns = [
    # path("v1/", include(v1.urls)),
    path("v1/auth/signup/", signup, name="signup"),
    path("v1/auth/token/", token, name="login"),
    path("v1/auth/code/", code, name="code"),
]
