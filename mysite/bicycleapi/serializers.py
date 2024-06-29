from rest_framework import serializers
from .models import Bicycle
from django.contrib.auth.models import User


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ["id", "name", "model", "status"]
