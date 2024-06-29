from rest_framework import serializers
from bicycleapi.models import Rental  # Импорт модели аренды из другого приложения


class RentalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["id", "bicycle", "start_time", "end_time", "cost"]
