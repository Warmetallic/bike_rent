from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from bicycleapi.models import Bicycle
from bicycleapi.serializers import BicycleSerializer


# Create your views here.
def index(request):
    return render(request, "rentalapi/home.html")


class BicycleListView(ModelViewSet):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "id",
        "name",
        "model",
        "status",
    ]

    search_fields = [
        "name",
        "model",
        "status",
    ]

    ordering_fields = [
        "id",
        "name",
        "model",
        "status",
    ]
