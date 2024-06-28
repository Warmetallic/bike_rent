from django.urls import path, include

from rest_framework.routers import DefaultRouter

# from .views import home
from .views import (
    UserRegistrationAPIView,
    hello_world_view,
    UserViewSet,
    UserLoginAPIView,
)


app_name = "myauthapi"

routers = DefaultRouter()
routers.register("users", UserViewSet, basename="users")

urlpatterns = [
    # path("", home, name="home"),
    path("hello/", hello_world_view, name="hello"),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("", include(routers.urls)),
]
