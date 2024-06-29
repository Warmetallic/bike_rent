from django.urls import path
from bicycleapi.views import index

app_name = "rentalapi"

urlpatterns = [
    path("", index, name="index"),
]
