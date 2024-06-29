from django.urls import path, include

from rest_framework.routers import DefaultRouter

# from .views import home
from .views import (
    UserViewSet,
    UserLoginAPIView,
)


app_name = "myauthapi"

routers = DefaultRouter()
routers.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("", include(routers.urls)),
]
