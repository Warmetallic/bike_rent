from django.urls import path
from rentalapi.views import index

app_name = "rentalapi"

urlpatterns = [
    path("", index, name="index"),
]
