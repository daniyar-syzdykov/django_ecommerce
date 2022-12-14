import uuid
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(blank=True)
