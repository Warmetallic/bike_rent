from django.urls import path
from .views import RentalHistoryView

urlpatterns = [
    path("history/", RentalHistoryView.as_view(), name="rental-history"),
]
