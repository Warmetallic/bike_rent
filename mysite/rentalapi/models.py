from django.db import models
from django.contrib.auth.models import User


class Bicycle(models.Model):
    status_choices = []
