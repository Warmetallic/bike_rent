from django.db import models
from django.contrib.auth.models import User


class Bicycle(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    status_choices = [("available", "Available"), ("rented", "Rented")]
    status = models.CharField(
        max_length=10, choices=status_choices, default="available"
    )


# class Rental(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
