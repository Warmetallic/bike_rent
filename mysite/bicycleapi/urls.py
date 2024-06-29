from django.urls import path, include
from bicycleapi.views import BicycleListView, BicycleRental, BicycleReturn
from rest_framework.routers import DefaultRouter

app_name = "bicycleapi"

routers = DefaultRouter()
routers.register("bicycle", BicycleListView, basename="bicycle-list")


urlpatterns = [
    path("rent/", BicycleRental.as_view(), name="rent"),
    path("return/", BicycleReturn.as_view(), name="return"),
    path("", include(routers.urls)),
]
