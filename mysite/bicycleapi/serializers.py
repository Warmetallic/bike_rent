from rest_framework import serializers
from .models import Bicycle
from django.contrib.auth.models import User


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ["id", "name", "model", "status"]


class BicycleRentalSerializer(serializers.Serializer):
    bicycle_id = serializers.IntegerField(help_text="ID of the bicycle to rent")


class BicycleReturnSerializer(serializers.Serializer):
    rental_id = serializers.IntegerField(help_text="ID of the rental to return")
