from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  # Country value is currency and the display is country iso code
  country = models.CharField(max_length=3,
    choices=(("GBP", "GB"), ("EUR", "DE"), ("DKK", "DK"), ("MXN", "MX"), ("SGD", "SG")))
